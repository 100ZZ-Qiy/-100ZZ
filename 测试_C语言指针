#include <stdio.h>
/*  实现过程：
   1.输出排序前的数组
    printf("排序前的数组:\n");
    printShuZu（  .... ）;//调用输出函数
    
    2. 对数组进行冒泡排序
    bubbleSort（  .... ）;//调用冒泡排序函数

    3.输出排序后的数组
    printf("排序后的数组:\n");
    printShuZu（  .... ）;//调用输出函数
*/
void bubbleSort(int *p, int n);
void printShuZu(int *p, int n);
void bubbleSort(int *p, int n) {
    int i, j, t;
    for (i = 0; i < n - 1; i++) {
        for (j = 0; j < n - 1 - i; j++) {
            if (*(p + j) > *(p + j + 1)) {
                t = *(p + j);
                *(p + j) = *(p + j + 1);
                *(p + j + 1) = t;
            }
        }
    }
}
void printShuZu(int *p, int n) {
    for (int i = 0; i < n; i++) {
        printf("%d ", *(p + i));
    }
    printf("\n");
}

int main() {
    int n;                  
    int a[100];             
    int *p = a;             
    
    printf("请输入障碍物数量：");
    scanf("%d", &n);
    printf("请输入%d个距离值：", n);
    for (int i = 0; i < n; i++) {
        scanf("%d", p + i);
    }
    
	printf("排序前的数组:\n");
    printShuZu(p, n);
    bubbleSort(p, n);
    printf("排序后的数组:\n");
    printShuZu(p, n);
    
    return 0;
}
