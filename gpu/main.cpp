#include <iostream>
#include <fstream>
#include <vector>
#include <time.h>
#include <random>
#include "cl.hpp"

using namespace std;

template <class T>
T select(vector<T> variants, size_t cl_info) {
    cout << "Select:" << endl;

    for (int i = 0; i < variants.size(); i++) {
        string name;
        variants[i].getInfo(cl_info, &name);
        cout << i << ": " << name << endl;
    }

    size_t select;
    cin >> select;
    return variants[select];
}

inline string loadProgram(const string& input)
{
    ifstream stream(input);
    if (!stream.is_open()) {
        cout << "Can`t open file: " << input << endl;
        exit(1);
    }
    return string(istreambuf_iterator<char>(stream), (istreambuf_iterator<char>()));
}



int main() {
    const size_t SIZE = 512;

    std::vector<cl::Platform> all_platforms;
    cl::Platform::get(&all_platforms);
    cl::Platform default_platform=select(all_platforms, CL_PLATFORM_NAME);


    std::vector<cl::Device> all_devices;
    default_platform.getDevices(CL_DEVICE_TYPE_ALL, &all_devices);
    cl::Device device=select(all_devices, CL_DEVICE_NAME);


    cl::Context context({device});
    cl::Program program(context, loadProgram("kernel.cl"));
    program.build({device});

    vector<int> matrix_a(SIZE, 100);
    vector<int> matrix_b(SIZE, 200);
    vector<int> matrix_c(SIZE, 0);

    cl::Buffer buffer_a(context, CL_MEM_READ_ONLY, sizeof(int)*SIZE);
    cl::Buffer buffer_b(context, CL_MEM_WRITE_ONLY, sizeof(int)*SIZE);
    cl::Buffer buffer_c(context, CL_MEM_WRITE_ONLY, sizeof(int)*SIZE);

    cl::CommandQueue queue(context,device);

    queue.enqueueWriteBuffer(buffer_a, CL_TRUE, 0, sizeof(int)*SIZE, &matrix_a[0]);
    queue.enqueueWriteBuffer(buffer_b, CL_TRUE, 0, sizeof(int)*SIZE, &matrix_b[0]);

    cl::Kernel kernel_add = cl::Kernel(program,"simple_add");
    kernel_add.setArg(0, buffer_a);
    kernel_add.setArg(1, buffer_b);
    kernel_add.setArg(2, buffer_c);

    size_t work_size_multiple;
    kernel_add.getWorkGroupInfo(device, CL_KERNEL_PREFERRED_WORK_GROUP_SIZE_MULTIPLE, &work_size_multiple);

    queue.enqueueNDRangeKernel(kernel_add, cl::NullRange, cl::NDRange(128), work_size_multiple * 4);
    queue.finish();


    queue.enqueueReadBuffer(buffer_c, CL_TRUE, 0, sizeof(int)*SIZE, &matrix_c[0]);

    for (int i : matrix_c) {
        std::cout << i << " ";
    }

    return 0;
}