import subprocess
import os
import sys

try:
    import docker
    import json
    import tarfile
    import io
    import time

except ImportError:
    has_docker = False
else:
    has_docker = True


class SimpleExecutable(object):
    """Wrapper for external executable.

    .. py::attribute:: name
        (string) The name of the program (human readable).

    .. py::attribute:: path
        (string) The path pointing to the executable.

    .. py::attribute:: description
        (None or string) Describing the function of the executable,
        possibly with input and output specified.

    .. py::attribute:: parameters
        (None or function) Should be a function taking one argument,
        returning a list of strings. This list is then passed as
        command-line arguments to the executable. This function should
        be able to handle `None` as an argument.
    """
    def __init__(self, name, description, path,
                 working_dir=None, parameters=None):
        self.name = name
        self.path = path
        self.description = description
        self.working_dir = working_dir
        self.parameters = parameters

    def run(self, args_obj=None, **kwargs):
        """Call `subprocess.run`.

        :param args_obj:
            Object containing information for arguments. This is passed
            through the :py:attribute:`parameters` function attribute to
            generate the list of command-line arguments.
        :type args_obj: Any

        :param **kwargs:
            Keyword arguments are passed to `subprocess.run`.

        :return:
            CompletedProcess object.
        """
        if self.working_dir:
            orig_wd = os.getcwd()
            os.chdir(self.working_dir)

        args = [self.path]
        if self.parameters:
            args.extend(self.parameters(args_obj))

        result = subprocess.run(args, **kwargs)

        if self.working_dir:
            os.chdir(orig_wd)

        return result


def build_image(client: docker.Client, path: str, name: str):
    """Build the Docker image as per Dockerfile present in <path>.
    If the docker image with given name is newer than the Dockerfile,
    nothing is done.

    :param client:
        Docker client
    :param path:
        Location of Dockerfile
    :param name:
        Name of the image
    """
    assert os.path.exists(path + '/Dockerfile')
    time = os.stat(path + '/Dockerfile').st_mtime

    il = client.images(name=name)
    if len(il) == 0 or il[0]['Created'] < time:
        response = client.build(path, tag=name, rm=True)
        for json_bytes in response:
            line = json.loads(json_bytes.decode())['stream']
            print(line, end='', file=sys.stderr, flush=True)


class Archive(object):
    """Easy interface to `tarfile`.

    We use buffered `tar` files to communicate with Docker
    containers. This class provides an easy way to create
    `tar` buffers on the fly, or read from them.

    Methods in this class can be chained JS style."""
    def __init__(self, mode, data=None):
        self.file = io.BytesIO(data)
        self.tar = tarfile.open(mode=mode, fileobj=self.file)

    def add_text_file(self, filename: str, text: str, encoding='utf-8'):
        """Add the contents of `text` to a new entry in the `tar`
        file.

        :return:
            self
        """
        b = text.encode(encoding)
        f = io.BytesIO(b)
        info = tarfile.TarInfo(filename)
        info.size = len(b)
        info.type = tarfile.REGTYPE
        info.mtime = time.time()

        self.tar.addfile(info, fileobj=f)
        return self

    def get_text_file(self, filename: str, encoding='utf-8') -> str:
        """Read the contents of a file in the archive.

        :return:
            contents of file in string.
        """
        f = self.tar.extractfile(filename)
        if f:
            return f.read().decode(encoding)
        return None

    def close(self):
        self.tar.close()
        return self

    def __iter__(self):
        return iter(self.tar.getmembers())

    @property
    def buffer(self):
        return self.file.getvalue()


class DockerContainer(object):
    """Easy interface to Docker API.

    This class encapsulates a part of the Docker API, with the goal
    of making it easier to start a container, add some files, run a
    few scripts, read the output, and then remove the container
    again.

    The object is a context manager for the created Docker container,
    in that it starts the container upon entry and exterminates the
    same container upon exit.
    """

    client = docker.Client()

    def __init__(self, image, working_dir=None):
        self.image = image
        self.working_dir = working_dir

        container = self.client.create_container(
            image=image, detach=True, stdin_open=True,
            working_dir=working_dir)
        self.container_id = container['Id']

    def put_archive(self, archive, path="."):
        """Put the contents of an archive into the Docker container.

        :param archive:
            The `Archive` instance that contains the files that need
            to be injected.
        :type archive: Archive

        :param path:
            Where to extract the archive within the container.
        :type path: str
        """
        if self.working_dir is not None:
            path = os.path.join(self.working_dir, path)

        self.client.put_archive(
            self.container_id, path, archive.buffer)

    def get_archive(self, path):
        """Get a file or directory from the container and make it into
        an `Archive` object."""
        if self.working_dir is not None and not os.path.isabs(path):
            path = os.path.join(self.working_dir, path)

        strm, stat = self.client.get_archive(
            self.container_id, path)

        return Archive('r', strm.read())

    def run(self, cmd, **kwargs):
        """Run a command.

        :param cmd:
            Command to be run and arguments as a list.
        :type cmd: List[str]

        :param kwargs:
            Forwarded to Docker-py `exec_create` function call.

        :return:
            Output of command.
        :rtype: bytes
        """
        exe = self.client.exec_create(
            container=self.container_id,
            cmd=cmd, **kwargs)

        return self.client.exec_start(exec_id=exe['Id'])

    def sh(self, *cmds):
        """Run a command with `sh -c`."""
        return self.run(['sh', '-c', ' && '.join(cmds)])

    def start(self):
        self.client.start(container=self.container_id)

    def kill(self):
        self.client.kill(self.container_id)

    def remove(self, force=False):
        self.client.remove_container(self.container_id, force=force)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, exc_st):
        self.kill()
        self.remove()
