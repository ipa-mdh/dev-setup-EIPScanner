from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
import subprocess


class EipScannerRecipe(ConanFile):
    name = "dev-setup-eipscanner"
    version = "1.0"

    # Optional metadata
    license = "<Put the package license here>"
    author = "<Put your name here> <And your email here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of hello package here>"
    topics = ("<Put some tag here>", "<here>", "<and here>")

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    # Sources are located in the same place as this recipe, copy them to the recipe
    exports_sources = "EIPScanner/CMakeLists.txt", "EIPScanner/src/*", "EIPScanner/include/*", "EIPScanner/EIPScanner.pc.in"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def layout(self):
        cmake_layout(self)

    def source(self):
        self.output.info("Updating git submodules recursively...")
        subprocess.run(["git", "submodule", "update", "--init", "--recursive"], check=True)

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)
        # tc.cache_variables["CMAKE_BUILD_TYPE"] = "Release"
        # tc.generator = "Unix Makefiles"
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure(build_script_folder="EIPScanner")
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["hello"]

    def requirements(self):
        self.requires("gtest/1.14.0")