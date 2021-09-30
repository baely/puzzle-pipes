//
// Created by Bailey on 30/09/2021.
//

#include <stdio.h>


void update_list(int* g) {
    g[1] = 10;
}

int main() {
    int a[5] = {0, 0, 0, 0, 0};
    a[0] = 2;
    a[1] = 5;

    for (int i = 0; i < 5; i++) {
        printf("%d\n", a[i]);
    }

    update_list(a);

    for (int i = 0; i < 5; i++) {
        printf("%d\n", a[i]);
    }
}
