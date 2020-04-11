import setuptools

setuptools.setup(
        name="wimund",
        version="0.1",
        author="Adam Olech",
        author_email="nddr89@gmail.com",
        description="Helper utility for mounting sshfs mounts in PyQt",
        #url="",
        packages=["wimund"],
        python_requires='>=3.6',
        entry_points={
            "console_scripts": ["wimund = wimund:main"]
            },
        install_requires=["requests", "pyperclip", "prettytable", "pygments"],
        )
