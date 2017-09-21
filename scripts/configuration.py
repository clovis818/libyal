# -*- coding: utf-8 -*-
"""The project configuration."""

from __future__ import unicode_literals

import json
import logging
import os

try:
  import ConfigParser as configparser
except ImportError:
  import configparser  # pylint: disable=import-error

import errors


class ProjectConfiguration(object):
  """Project configuration.

  Attributes:
    coverty_scan_token (str): scan token for Coverty Scan (scan.coverity.com).
    cygwin_build_dependencies (str): Cygwin build dependencies.
    dpkg_build_dependencies (str): dpkg build dependencies.
    gcc_build_dependencies (list[str]): GCC build dependencies.
    gcc_static_build_dependencies (list[str]): GCC build dependencies for
        building static binaries.
    library_build_dependencies (str): library build dependencies.
    library_description (str): description of the library.
    library_name (str): name of the library.
    library_name_suffix (str): suffix of the name of the library.
    library_public_types (str): types publicly exported by the library.
    mingw_build_dependencies (list[str]): MinGW build dependencies.
    mingw_dll_dependencies (list[str]): MinGW DLL dependencies.
    mingw_dll_filename (str): name of the MinGW DLL file.
    mingw_msys_build_dependencies (str): MinGW-MSYS build dependencies.
    msvscpp_build_dependencies (str): Visual Studio build dependencies.
    msvscpp_dll_dependencies (list[str]): Visual Studio DLL dependencies.
    project_authors (str): authors of the project.
    project_description (str): description of the project.
    project_documenation_url (str): URL of the documentation of the project.
    project_downloads_url (str): URL of the downloads of the project.
    project_git_url (str): URL of the git repository of the project.
    project_name (str): name of the project, such as "libyal".
    project_status (str): status of the project, such as "experimental".
    project_year_of_creation (str): year the project was created.
    python_module_authors (str): authors of the Python module.
    python_module_name (str): name of the Python module, such as "pyyal".
    python_module_year_of_creation (str): year the Python module was created.
    rpm_build_dependencies (str): rpm build dependencies.
    supports_debug_output (bool): True if the project supports debug output.
    tests_authors (str): authors of the test files.
    tests_example_filename1 (str): name of the first test example filename.
    tests_example_filename2 (str): name of the second test example filename.
    tests_options (str): option sets used by the tests.
    tests_profiles (list[str]): names of the test profiles.
    tools_authors (str): authors of the tools.
    tools_build_dependencies (str): tools build dependencies.
    tools_description (str): description of the tools.
    tools_directory (str): name of the directory that contains the tools.
    tools_names (str): names of the individual tools.
  """

  def __init__(self):
    """Initializes a project configuation."""
    super(ProjectConfiguration, self).__init__()
    self._configuration_file_path = None
    self._has_dpkg = None
    self._has_rpm = None
    self._has_python_module = None
    self._has_tests = None
    self._has_tools = None

    # Project configuration.
    self.project_authors = None
    self.project_description = None
    self.project_documentation_url = None
    self.project_downloads_url = None
    self.project_git_url = None
    self.project_name = None
    self.project_status = None
    self.project_year_of_creation = None

    # Functionality the project offsers.
    self.supports_debug_output = False

    # Library configuration.
    self.library_build_dependencies = None
    self.library_description = None
    self.library_name = None
    self.library_name_suffix = None
    # TODO: determine public types based on include header.
    self.library_public_types = None

    # Python module configuration.
    self.python_module_authors = None
    self.python_module_name = None
    self.python_module_year_of_creation = None

    # Tools configuration.
    self.tools_authors = None
    self.tools_build_dependencies = None
    self.tools_description = None
    self.tools_directory = None
    self.tools_names = []

    # Tests configuration.
    self.tests_authors = None
    self.tests_options = None
    self.tests_profiles = None
    self.tests_example_filename1 = None
    self.tests_example_filename2 = None

    # GCC specific configuration.
    self.gcc_build_dependencies = None
    self.gcc_static_build_dependencies = None

    # Cygwin specific configuration.
    self.cygwin_build_dependencies = None
    self.cygwin_dll_dependencies = None
    self.cygwin_dll_filename = None

    # MinGW specific configuration.
    self.mingw_build_dependencies = None
    self.mingw_dll_dependencies = None
    self.mingw_dll_filename = None

    # MinGW-MSYS specific configuration.
    self.mingw_msys_build_dependencies = None

    # DPKG specific configuration.
    self.dpkg_build_dependencies = None

    # Visual Studio specific configuration.
    self.msvscpp_build_dependencies = None
    self.msvscpp_dll_dependencies = None

    # RPM specific configuration.
    self.rpm_build_dependencies = None

    # Coverty configuration.
    self.coverty_scan_token = None

    # TODO: add attributes below to docstring.

    # Development configuration.
    self.development_main_object = None
    self.development_main_object_filename = None
    self.development_main_object_pre_open_python = None
    self.development_main_object_post_open_python = None
    self.development_main_object_post_open_file_object_python = None
    self.development_main_object_size = None
    self.development_glob = False
    self.development_pytsk3 = False

    # Troubleshooting configuration.
    self.troubleshooting_example = None

    # Mount tool configuration.
    self.mount_tool_additional_arguments = None
    self.mount_tool_missing_backend_error = None
    self.mount_tool_mount_point = None
    self.mount_tool_mounted_description = None
    self.mount_tool_mounted_dokan = None
    self.mount_tool_mounted_fuse = None
    self.mount_tool_source = None
    self.mount_tool_source_description = None
    self.mount_tool_source_description_long = None
    self.mount_tool_source_type = None

  def _GetConfigValue(self, config_parser, section_name, value_name):
    """Retrieves a value from the config parser.

    Args:
      config_parser (ConfigParser): configuration parser.
      section_name (str): name of the section that contains the value.
      value_name (name): name of the value.

    Returns:
      object: value.
    """
    return json.loads(config_parser.get(section_name, value_name))

  def _GetOptionalConfigValue(
      self, config_parser, section_name, value_name, default_value=None):
    """Retrieves an optional configuration value from the config parser.

    Args:
      config_parser (ConfigParser): configuration parser.
      section_name (str): name of the section that contains the value.
      value_name (name): name of the value.
      default_value (Optional[object]): default value.

    Returns:
      object: value or default value if not available.
    """
    try:
      return self._GetConfigValue(config_parser, section_name, value_name)
    except (configparser.NoOptionError, configparser.NoSectionError):
      return default_value

  def _ReadCygwinConfiguration(self, config_parser):
    """Reads the Cygwin configuration.

    Args:
      config_parser (ConfigParser): configuration file parser.
    """
    self.cygwin_build_dependencies = self._GetOptionalConfigValue(
        config_parser, 'cygwin', 'build_dependencies', default_value=[])
    self.cygwin_dll_dependencies = self._GetOptionalConfigValue(
        config_parser, 'cygwin', 'dll_dependencies', default_value=[])

    cygwin_dll_filename = 'cyg{0:s}-0.dll'.format(self.library_name_suffix)
    self.cygwin_dll_filename = self._GetOptionalConfigValue(
        config_parser, 'cygwin', 'dll_filename',
        default_value=cygwin_dll_filename)

    # Remove trailing comments.
    self.cygwin_build_dependencies = [
        name.split(' ')[0] for name in self.cygwin_build_dependencies]

  def _ReadDevelopmentConfiguration(self, config_parser):
    """Reads the development configuration.

    Args:
      config_parser (ConfigParser): configuration file parser.
    """
    if not config_parser.has_section('development'):
      return

    features = self._GetOptionalConfigValue(
        config_parser, 'development', 'features', default_value=[])

    if features:
      self.development_glob = 'glob' in features
      self.development_pytsk3 = 'pytsk3' in features

    self.development_main_object = self._GetConfigValue(
        config_parser, 'development', 'main_object')

    self.development_main_object_filename = self._GetConfigValue(
        config_parser, 'development', 'main_object_filename')

    self.development_main_object_size = self._GetOptionalConfigValue(
        config_parser, 'development', 'main_object_size')

    self.development_main_object_pre_open_python = (
        self._GetOptionalConfigValue(
            config_parser, 'development', 'main_object_pre_open_python'))

    self.development_main_object_post_open_python = (
        self._GetOptionalConfigValue(
            config_parser, 'development', 'main_object_post_open_python'))

    self.development_main_object_post_open_file_object_python = (
        self._GetOptionalConfigValue(
            config_parser, 'development',
            'main_object_post_open_file_object_python'))

  def _ReadDPKGConfiguration(self, config_parser):
    """Reads the DPKG configuration.

    Args:
      config_parser (ConfigParser): configuration file parser.
    """
    self.dpkg_build_dependencies = self._GetOptionalConfigValue(
        config_parser, 'dpkg', 'build_dependencies', default_value=[])

    # Remove trailing comments.
    self.dpkg_build_dependencies = [
        name.split(' ')[0] for name in self.dpkg_build_dependencies]

  def _ReadGCCConfiguration(self, config_parser):
    """Reads the GCC configuration.

    Args:
      config_parser (ConfigParser): configuration file parser.
    """
    self.gcc_build_dependencies = self._GetOptionalConfigValue(
        config_parser, 'gcc', 'build_dependencies', default_value=[])
    self.gcc_static_build_dependencies = self._GetOptionalConfigValue(
        config_parser, 'gcc', 'static_build_dependencies', default_value=[])

    # Remove trailing comments.
    self.gcc_build_dependencies = [
        name.split(' ')[0] for name in self.gcc_build_dependencies]
    self.gcc_static_build_dependencies = [
        name.split(' ')[0] for name in self.gcc_static_build_dependencies]

  def _ReadLibraryConfiguration(self, config_parser):
    """Reads the library configuration.

    Args:
      config_parser (ConfigParser): configuration file parser.
    """
    self.library_description = self._GetConfigValue(
        config_parser, 'library', 'description')
    self.library_build_dependencies = self._GetOptionalConfigValue(
        config_parser, 'library', 'build_dependencies', default_value=[])
    self.library_name = self.project_name
    self.library_name_suffix = self.library_name[3:]
    self.library_public_types = self._GetOptionalConfigValue(
        config_parser, 'library', 'public_types', default_value=[])

    # Remove trailing comments.
    self.library_build_dependencies = [
        name.split(' ')[0] for name in self.library_build_dependencies]

  def _ReadMinGWConfiguration(self, config_parser):
    """Reads the MinGW configuration.

    Args:
      config_parser (ConfigParser): configuration file parser.
    """
    self.mingw_build_dependencies = self._GetOptionalConfigValue(
        config_parser, 'mingw', 'build_dependencies', default_value=[])
    self.mingw_dll_dependencies = self._GetOptionalConfigValue(
        config_parser, 'mingw', 'dll_dependencies', default_value=[])

    mingw_dll_filename = 'lib{0:s}-1.dll'.format(self.library_name_suffix)
    self.mingw_dll_filename = self._GetOptionalConfigValue(
        config_parser, 'mingw', 'dll_filename',
        default_value=mingw_dll_filename)

    # Remove trailing comments.
    self.mingw_build_dependencies = [
        name.split(' ')[0] for name in self.mingw_build_dependencies]

  def _ReadMinGWMSYSConfiguration(self, config_parser):
    """Reads the MinGW-MSYS configuration.

    Args:
      config_parser (ConfigParser): configuration file parser.
    """
    self.mingw_msys_build_dependencies = self._GetOptionalConfigValue(
        config_parser, 'mingw_msys', 'build_dependencies', default_value=[])

    # Remove trailing comments.
    self.mingw_msys_build_dependencies = [
        name.split(' ')[0] for name in self.mingw_msys_build_dependencies]

  def _ReadMountToolConfiguration(self, config_parser):
    """Reads the mount tool configuration.

    Args:
      config_parser (ConfigParser): configuration file parser.
    """
    if not config_parser.has_section('mount_tool'):
      return

    self.mount_tool_additional_arguments = self._GetOptionalConfigValue(
        config_parser, 'mount_tool', 'additional_arguments')

    self.mount_tool_missing_backend_error = self._GetConfigValue(
        config_parser, 'mount_tool', 'missing_backend_error')
    self.mount_tool_mount_point = self._GetConfigValue(
        config_parser, 'mount_tool', 'mount_point')
    self.mount_tool_mounted_description = self._GetConfigValue(
        config_parser, 'mount_tool', 'mounted_description')
    self.mount_tool_mounted_dokan = self._GetConfigValue(
        config_parser, 'mount_tool', 'mounted_dokan')
    self.mount_tool_mounted_fuse = self._GetConfigValue(
        config_parser, 'mount_tool', 'mounted_fuse')
    self.mount_tool_source = self._GetConfigValue(
        config_parser, 'mount_tool', 'source')
    self.mount_tool_source_description = self._GetConfigValue(
        config_parser, 'mount_tool', 'source_description')

    # If the long source description is not set it will default to
    # source description.
    self.mount_tool_source_description_long = self._GetOptionalConfigValue(
        config_parser, 'mount_tool', 'source_description_long')

    self.mount_tool_source_type = self._GetConfigValue(
        config_parser, 'mount_tool', 'source_type')

    if self.mount_tool_source_type not in ['image', 'volume']:
      raise errors.ConfigurationError(
          'unsupported mount tool source type: {0:s}'.format(
              self.mount_tool_source_type))

  def _ReadProjectConfiguration(self, config_parser):
    """Reads the project configuration.

    Args:
      config_parser (ConfigParser): configuration file parser.

    Raises:
      ConfigurationError: if the project year of creation cannot
          be converted to a base 10 integer value.
    """
    self.project_name = self._GetConfigValue(
        config_parser, 'project', 'name')

    project_authors = ['Joachim Metz <joachim.metz@gmail.com>']
    self.project_authors = self._GetOptionalConfigValue(
        config_parser, 'project', 'authors', default_value=project_authors)

    self.project_documentation_url = self._GetOptionalConfigValue(
        config_parser, 'project', 'documentation_url')

    project_downloads_url = 'https://github.com/libyal/{0:s}/releases'.format(
        self.project_name)
    self.project_downloads_url = self._GetOptionalConfigValue(
        config_parser, 'project', 'downloads_url',
        default_value=project_downloads_url)

    project_git_url = 'https://github.com/libyal/{0:s}.git'.format(
        self.project_name)
    self.project_git_url = self._GetOptionalConfigValue(
        config_parser, 'project', 'git_url', default_value=project_git_url)

    self.project_status = self._GetConfigValue(
        config_parser, 'project', 'status')
    self.project_year_of_creation = self._GetConfigValue(
        config_parser, 'project', 'year_of_creation')

    try:
      self.project_year_of_creation = int(self.project_year_of_creation, 10)
    except ValueError:
      raise errors.ConfigurationError(
          'Invalid project year of creation: {0!s}'.format(
              self.project_year_of_creation))

    features = self._GetOptionalConfigValue(
        config_parser, u'project', u'features', default_value=[])

    self.supports_debug_output = 'debug_output' in features

  def _ReadPythonModuleConfiguration(self, config_parser):
    """Reads the Python module configuration.

    Args:
      config_parser (ConfigParser): configuration file parser.

    Raises:
      ConfigurationError: if the Python module year of creation cannot
          be converted to a base 10 integer value.
    """
    self.python_module_authors = self._GetOptionalConfigValue(
        config_parser, 'python_module', 'authors',
        default_value=self.project_authors)
    self.python_module_name = 'py{0:s}'.format(self.library_name_suffix)
    self.python_module_year_of_creation = self._GetOptionalConfigValue(
        config_parser, 'python_module', 'year_of_creation')

    if not self.python_module_year_of_creation:
      self.python_module_year_of_creation = self.project_year_of_creation
    else:
      try:
        self.python_module_year_of_creation = int(
            self.python_module_year_of_creation, 10)
      except ValueError:
        raise errors.ConfigurationError(
            'Invalid Python module year of creation: {0!s}'.format(
                self.python_module_year_of_creation))

  def _ReadRPMConfiguration(self, config_parser):
    """Reads the RPM configuration.

    Args:
      config_parser (ConfigParser): configuration file parser.
    """
    self.rpm_build_dependencies = self._GetOptionalConfigValue(
        config_parser, 'rpm', 'build_dependencies', default_value=[])

    # Remove trailing comments.
    self.rpm_build_dependencies = [
        name.split(' ')[0] for name in self.rpm_build_dependencies]

  def _ReadTestsConfiguration(self, config_parser):
    """Reads the tests configuration.

    Args:
      config_parser (ConfigParser): configuration file parser.
    """
    self.tests_authors = self._GetOptionalConfigValue(
        config_parser, 'tests', 'authors', default_value=self.project_authors)
    self.tests_options = self._GetOptionalConfigValue(
        config_parser, 'tests', 'options', default_value=[])
    self.tests_profiles = self._GetOptionalConfigValue(
        config_parser, 'tests', 'profiles', default_value=[])
    self.tests_example_filename1 = self._GetOptionalConfigValue(
        config_parser, 'tests', 'example_filename1')
    self.tests_example_filename2 = self._GetOptionalConfigValue(
        config_parser, 'tests', 'example_filename2')

  def _ReadToolsConfiguration(self, config_parser):
    """Reads the tools configuration.

    Args:
      config_parser (ConfigParser): configuration file parser.
    """
    self.tools_authors = self._GetOptionalConfigValue(
        config_parser, 'tools', 'authors', default_value=self.project_authors)
    self.tools_build_dependencies = self._GetOptionalConfigValue(
        config_parser, 'tools', 'build_dependencies', default_value=[])
    self.tools_description = self._GetOptionalConfigValue(
        config_parser, 'tools', 'description', default_value='')

    tools_directory = '{0:s}tools'.format(self.library_name_suffix)
    self.tools_directory = self._GetOptionalConfigValue(
        config_parser, 'tools', 'directory', default_value=tools_directory)

    self.tools_names = self._GetOptionalConfigValue(
        config_parser, 'tools', 'names', default_value=[])

    # Remove trailing comments.
    self.tools_build_dependencies = [
        name.split(' ')[0] for name in self.tools_build_dependencies]

  def _ReadTroubleshootingConfiguration(self, config_parser):
    """Reads the troubleshooting configuration.

    Args:
      config_parser (ConfigParser): configuration file parser.
    """
    if not config_parser.has_section('troubleshooting'):
      return

    self.troubleshooting_example = self._GetOptionalConfigValue(
        config_parser, 'troubleshooting', 'example')

  def _ReadVisualStudioConfiguration(self, config_parser):
    """Reads the Visual Studio configuration.

    Args:
      config_parser (ConfigParser): configuration file parser.
    """
    self.msvscpp_build_dependencies = self._GetOptionalConfigValue(
        config_parser, 'msvscpp', 'build_dependencies', default_value=[])
    self.msvscpp_dll_dependencies = self._GetOptionalConfigValue(
        config_parser, 'msvscpp', 'dll_dependencies', default_value=[])

    # Remove trailing comments.
    self.msvscpp_build_dependencies = [
        name.split(' ')[0] for name in self.msvscpp_build_dependencies]

  def HasDebugOutput(self):
    """Determines if the project provides debug output.

    Returns:
      bool: True if the project provides debug output.
    """
    return self.supports_debug_output

  def HasDependencyBzip2(self):
    """Determines if the project depends on bzip2.

    Returns:
      bool: True if the project depends on bzip2.
    """
    return 'bzip2' in self.library_build_dependencies

  def HasDependencyDokan(self):
    """Determines if the project depends on Dokan.

    Returns:
      bool: True if the project depends on Dokan.
    """
    return (self.HasDependencyFuse() or
            'dokan' in self.msvscpp_build_dependencies)

  def HasDependencyFuse(self):
    """Determines if the project depends on fuse.

    Returns:
      bool: True if the project depends on fuse.
    """
    return 'fuse' in self.tools_build_dependencies

  def HasDependencyLex(self):
    """Determines if the project depends on lex.

    Returns:
      bool: True if the project depends on lex.
    """
    return 'lex' in self.library_build_dependencies

  def HasDependencyYacc(self):
    """Determines if the project depends on yacc.

    Returns:
      bool: True if the project depends on yacc.
    """
    return 'yacc' in self.library_build_dependencies

  def HasDpkg(self):
    """Determines if the project provides dpkg configuration files.

    Returns:
      bool: True if the dpkg directory exits.
    """
    if self._has_dpkg is None:
      path = os.path.join(self._configuration_file_path, 'dpkg')
      self._has_dpkg = os.path.exists(path)

    return self._has_dpkg

  def HasDotNetBinding(self):
    """Determines if the project provides a .net binding.

    Returns:
      bool: True if the .net binding directory exits.
    """
    return False

  def HasJavaBinding(self):
    """Determines if the project provides a Java binding.

    Returns:
      bool: True if the Java binding directory exits.
    """
    return False

  def HasPythonModule(self):
    """Determines if the project provides a Python module.

    Returns:
      bool: True if the Python module directory exits.
    """
    if self._has_python_module is None:
      path = os.path.join(
          self._configuration_file_path, self.python_module_name)
      self._has_python_module = os.path.exists(path)

    return self._has_python_module

  def HasRpm(self):
    """Determines if the project provides rpm configuration files.

    Returns:
      bool: True if the rpm spec file exits.
    """
    if self._has_rpm is None:
      spec_filename = '{0:s}.spec.in'.format(self.project_name)
      path = os.path.join(self._configuration_file_path, spec_filename)
      self._has_rpm = os.path.exists(path)

    return self._has_rpm

  def HasTests(self):
    """Determines if the project provides tests.

    Returns:
      bool: True if the tests directory exits.
    """
    if self._has_tests is None:
      path = os.path.join(self._configuration_file_path, 'tests')
      self._has_tests = os.path.exists(path)

    return self._has_tests

  def HasTools(self):
    """Determines if the project provides tools.

    Returns:
      bool: True if the tools directory exits.
    """
    if self._has_tools is None:
      path = os.path.join(self._configuration_file_path, self.tools_directory)
      self._has_tools = os.path.exists(path)

    return self._has_tools

  def ReadFromFile(self, filename):
    """Reads the configuration from file.

    Args:
      filename (str): path of the configuration file.
    """
    # TODO: replace by:
    # config_parser = configparser. ConfigParser(interpolation=None)
    config_parser = configparser.RawConfigParser()
    config_parser.read([filename])

    self._configuration_file_path = os.path.dirname(filename)

    self._ReadProjectConfiguration(config_parser)

    self._ReadLibraryConfiguration(config_parser)
    self._ReadPythonModuleConfiguration(config_parser)
    self._ReadToolsConfiguration(config_parser)
    self._ReadTestsConfiguration(config_parser)

    self._ReadDevelopmentConfiguration(config_parser)
    self._ReadTroubleshootingConfiguration(config_parser)

    self._ReadCygwinConfiguration(config_parser)
    self._ReadGCCConfiguration(config_parser)
    self._ReadMinGWConfiguration(config_parser)
    self._ReadMinGWMSYSConfiguration(config_parser)
    self._ReadVisualStudioConfiguration(config_parser)

    self._ReadDPKGConfiguration(config_parser)
    self._ReadRPMConfiguration(config_parser)

    self.coverty_scan_token = self._GetOptionalConfigValue(
        config_parser, 'coverty', 'scan_token', default_value='')

    self._ReadMountToolConfiguration(config_parser)
