#encoding:utf-8
import re
import sublime, sublime_plugin
import xml.etree.ElementTree as ET

exec_import = __import__("exec")

class PhingCommand(exec_import.ExecCommand):
  def run(self):
    self.project_root = self.window.folders()[0]
    buildfile = open("%s/build.xml" % self.project_root, 'r')
    file_content = buildfile.read()
    root = ET.fromstring(file_content)
    elements = root.findall(".//target")
    self.targets = map( lambda target: [target.attrib['name'], (target.attrib['description'] if target.attrib.has_key('description') else "No description given")], elements )
    self.targets.sort()
    self.window.show_quick_panel(self.targets, self.on_target)

  def on_target(self, index):
    if index != -1:
      command = "phing %s" % self.targets[index][0]
      self.window.run_command("exec", {
        "cmd": [command],
        "shell": True,
        "path": "/usr/local/bin:/opt/local/bin:/opt/local/sbin", #OSX additional path
        "working_dir": self.project_root
      })
