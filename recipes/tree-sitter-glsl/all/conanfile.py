from conan import ConanFile
from conan.tools.cmake import CMake, cmake_layout
from conan.tools.files import get, copy 

import os

required_conan_version = ">=2.4"


class TreeSitterCConan(ConanFile):
    name = "tree-sitter-glsl"
    description = "GLSL grammar for tree-sitter."
    license = "MIT"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://github.com/tree-sitter-grammars/tree-sitter-glsl"
    topics = ("parser", "grammar", "tree", "glsl", "ide")
    settings = "os", "arch", "compiler", "build_type"
    package_type = "library"

    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
    }
    implements = ["auto_shared_fpic"]
    languages = ["C"]
    exports_sources = "CMakeLists.txt"
    generators = "CMakeDeps", "CMakeToolchain"

    def layout(self):
        cmake_layout(self, src_folder="src")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def requirements(self):
        self.requires("tree-sitter/0.25.8", transitive_headers=True, transitive_libs=True)

    def build(self):
        cmake = CMake(self)
        cmake.configure(build_script_folder=os.path.join(self.source_folder,  os.pardir))
        cmake.build()

    def package(self):
        copy(
            self,
            "LICENSE",
            src=self.source_folder,
            dst=os.path.join(self.package_folder, "licenses"),
        )
        copy(
            self,
            "highlights.scm",
            src=os.path.join(self.source_folder, "queries"),
            dst=os.path.join(self.package_folder, "queries"),
        )
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["tree-sitter-glsl"]
