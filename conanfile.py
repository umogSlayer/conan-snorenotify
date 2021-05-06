from conans import ConanFile, CMake
from conans import tools
import os, shutil

class SnoreNotifyConan(ConanFile):
    name = 'snorenotify'
    version = '0.7.1'
    url = 'https://github.com/umogSlayer/conan-snorenotify'
    settings = 'os', 'compiler', 'build_type', 'arch'
    generators = 'cmake_paths'
    short_paths = True
    requires = [
        'qt/5.15.2@bincrafters/stable',
    ]
    build_requires = [
        'extra-cmake-modules/5.80.0',
    ]
    options = {
        'fPIC': [True, False],
    }
    default_options = {
        'fPIC': True,
        'qt:qtquickcontrols2': 'True',
        'qt:qtdeclarative': 'True',
        'qt:qttranslations': 'True',
        'qt:qtvirtualkeyboard': 'True',
        'qt:qtmultimedia': 'True',
        'qt:qtspeech': 'True',
    }
    exports = ["patches/*.patch"]

    def source(self):
        sources_git = tools.Git(folder='snorenotify')
        sources_git.clone('https://github.com/KDE/snorenotify.git')

    def build(self):
        tools.patch(base_path="snorenotify", patch_file="patches/snore_static_plugins.h.in.patch")
        tools.patch(base_path="snorenotify", patch_file="patches/plugincontainer.cpp.macos.patch")
        cmake = CMake(self)
        cmake_defs = {
            'CMAKE_PROJECT_SnoreNotify_INCLUDE': '../conan_paths.cmake',
            'CMAKE_POSITION_INDEPENDENT_CODE': '%s' % self.options.fPIC,
            'SNORE_STATIC': 'ON',
            'BUILD_SHARED_LIBS': 'OFF',
        }
        cmake.configure(defs=cmake_defs, source_dir='snorenotify')
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()
