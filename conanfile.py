from conans import ConanFile, CMake
from conans import tools
import os
import shutil
import glob

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
        'shared': [True, False],
    }
    default_options = {
        'fPIC': True,
        'shared': False,
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
            'CMAKE_POSITION_INDEPENDENT_CODE': 'ON' if self.options.fPIC else 'OFF',
            'SNORE_STATIC': 'OFF' if self.options.shared else 'ON',
            'BUILD_SHARED_LIBS': 'ON' if self.options.shared else 'OFF',
            'KDE_INSTALL_BUNDLEDIR': 'Applications/KDE',
        }
        cmake.configure(defs=cmake_defs, source_dir='snorenotify')
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()
        self.copy('*.a', dst='lib', keep_path=False)
        self.copy('*.lib', dst='lib', keep_path=False)
        tools.remove_files_by_mask(os.path.join(self.package_folder, "lib"), "*.cmake")

    def package_info(self):
        self.cpp_info.libs = ['snore-qt5', 'snoresettings-qt5']
        if not self.options.shared:
            for lib_file in glob.glob(os.path.join(self.package_folder, "lib", "liblibsnore_*_*.a")):
                lib = str(os.path.basename(lib_file)[3:-2])
                self.cpp_info.libs.append(lib)
            for lib_file in glob.glob(os.path.join(self.package_folder, "lib", "libsnore_*_*.lib")):
                lib = str(os.path.basename(lib_file)[:-4])
                self.cpp_info.libs.append(lib)
            self.cpp_info.defines.append('SNORE_STATIC')
