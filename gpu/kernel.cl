#define VALUES_PER_WORK_ITEM 64

void kernel simple_add(global const int* A, global const int* B, global int* C) {
    int localId = get_global_id(0);
    int groupId = get_group_id(0);
    int groupSize = get_local_size(0);

    for (int i = 0; i < VALUES_PER_WORK_ITEM; i++) {
        int index = groupId * groupSize * VALUES_PER_WORK_ITEM + i * groupSize + localId;
        C[index] = A[index] & B[index];
    }
}