# Development

To facilitate development and testing on a Raspberry Pi, files can be efficiently transferred using this command:

```bash
rsync --recursive \
  --progress \
  --archive \
  --exclude-from=.gitignore \
  --exclude=.git \
  --exclude=.gitignore \
   . user@ipaddress:~/dest/ 
```

> Do `cd` into the root folder of the project before using previous `rsync` command.

---

As a workaround to view threads in the 'Call Stack' section panel of Visual Studio Code, the following line in run_server.py:

```python
web.run_app(app, print=logger.info, port=port, host=host)
```

can be modified to:

```python
web.run_app(app, print=logger.info)
```

This modification retains the essential functionality without passing the port or host arguments, which don't allow setting custom port and host. Consequently, the server will start on default ones: port=8080 and host=0.0.0.0.".
