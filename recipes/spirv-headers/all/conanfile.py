from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout
from conan.tools.files import copy, get, rmdir
from conan.tools.scm import Version
import os

required_conan_version = ">2.0"


class SpirvheadersConan(ConanFile):
    name = "spirv-headers"
    homepage = "https://github.com/KhronosGroup/SPIRV-Headers"
    description = "Header files for the SPIRV instruction set."
    license = "MIT-KhronosGroup"
    topics = ("spirv", "spirv-v", "vulkan", "opengl", "opencl", "khronos")
    url = "https://github.com/conan-io/conan-center-index"
    package_type = "header-library"
    settings = "os", "arch", "compiler", "build_type"

    def layout(self):
        cmake_layout(self, src_folder="src")

    def package_id(self):
        self.info.clear()

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["SPIRV_HEADERS_SKIP_EXAMPLES"] = True
        tc.variables["SPIRV_HEADERS_ENABLE_TESTS"] = False
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        copy(self, "LICENSE*", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses"))
        cmake = CMake(self)
        cmake.install()
        rmdir(self, os.path.join(self.package_folder, "lib"))
        rmdir(self, os.path.join(self.package_folder, "share"))

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "SPIRV-Headers")
        self.cpp_info.set_property("cmake_target_name", "SPIRV-Headers::SPIRV-Headers")
        self.cpp_info.set_property("pkg_config_name", "SPIRV-Headers")
        self.cpp_info.bindirs = []
        self.cpp_info.libdirs = []

