/*
 * test.c
 * Zhaonian Zou
 * Harbin Institute of Technology
 * Jun 22, 2011
 */

#include <stdlib.h>
#include <stdio.h>
#include "extmem.h"
#include <time.h>
const int MAX = 1000;
Buffer buf;
unsigned char *blk;

int myRandom(int low,int high);
int store(unsigned int *blk,Buffer *buf);
int store2(unsigned int* blk, Buffer* buf,int start0,int start1,int tag);
int load(unsigned int *blk,Buffer *buf);
int selectAL(unsigned int *blk,Buffer *buf);
int projectionAL(unsigned int *blk,Buffer *buf);
int MergeSort(unsigned int addr,int n,Buffer *buf);
int Merge(unsigned int left,int lnum,unsigned int right,int rnum,Buffer *buf);
int split(unsigned int baseaddr,int num,int OFF,Buffer *buf);
int Nst_Loop_Join(unsigned int * blk,Buffer *buf);
void connectionAL(unsigned int * blk,Buffer *buf);
int main()
{
    int choice;
    srand((unsigned)time(NULL));
    if (!initBuffer(520, 64, &buf))
    {
        perror("Buffer Initialization Failed!\n");
        return -1;
    }
    //store(blk,&buf);
    load(blk,&buf);
    while(1){
        printf("========1:选择算法 2:投影算法 3:连接算法 4.集合并操作算法 -1:退出=======\n");
        scanf("%d",&choice);
        switch(choice){
            case 1:{
                selectAL(blk,&buf);
                break;
            }
            case 2:{
                projectionAL(blk,&buf);
                break;
            }
            case 3:{
                connectionAL(blk,&buf);
                break;
            }
            case 4:{
                break;
            }
            case -1:{
                return 0;
            }
            default:
            {
                printf("\t请输入合适的选项!\n\n");
                break;
            }
        }
    }
    return 0;
}
int myRandom(int low,int high){
    return low + rand()%(high - low + 1);
}

int store(unsigned int * blk,Buffer *buf){
    int i,j;
    for(i=0;i<16;i++){
        blk = getNewBlockInBuffer(buf);
        for(j=0;j<7;j++){
            int A = myRandom(1,40);
            int B = myRandom(1,1000);
            *(blk+2*j) = A;
            *(blk+2*j+1) = B;
            printf("R[%d][%d] = %d,%d\n",i,j,A,B);
        }
        *(blk+2*j) = i+1;
        if(i==15)
            *(blk+2*j) = 0;
        if (writeBlockToDisk(blk, i, buf) != 0){
            perror("Writing Block Failed!\n");
            return 0;
        }
        freeBlockInBuffer(blk,buf);
    }
    for(i=0;i<32;++i){
        blk = getNewBlockInBuffer(buf);
        for(j=0;j<7;++j){
            int c= myRandom(20,60);
            int d = myRandom(1,1000);
            *(blk+2*j)=c;
            *(blk+2*j+1)=d;
            printf("S[%d][%d] = %d,%d\n",i,j,c,d);
        }
        *(blk+2*j) = i+41;          //避免和之前的地址冲突
        if(i==31) *(blk+2*j) = 0;
        if (writeBlockToDisk(blk, i+40, buf) != 0){     //从40开始写
            perror("Writing Block Failed!\n");
            return 0;
        }
        freeBlockInBuffer(blk,buf);
    }
    return 1;
}
int load(unsigned int * blk,Buffer *buf){
    unsigned int a,b,c,d;
    int i,j;
    for(i=0;i<16;i++){
        printf("read blk addr:%d\n",i);
        if((blk = readBlockFromDisk(i,buf))==NULL){
            perror("Reading Block Failed!\n");
            return 0 ;
        }
        for(j=0;j<7;j++){
            a = *(blk+2*j);
            b = *(blk+2*j+1);
            printf("R[%d][%d] = %d,%d\n",i,j,a,b);
        }
        printf("next blk addr %d\n",*(blk+2*j));
        freeBlockInBuffer(blk,buf);
    }
    for(i=0;i<32;i++){
        printf("read blk addr:%d\n",i+40);
        if((blk = readBlockFromDisk(i+40,buf))==NULL){
            perror("Reading Block Failed!\n");
            return 0 ;
        }
         for(j=0;j<7;j++){
             c = *(blk+2*j);
             d = *(blk+2*j+1);
             printf("S[%d][%d] = %d,%d\n",i,j,c,d);
         }
         printf("next blk addr:%d\n",*(blk+2*j));
        freeBlockInBuffer(blk,buf);
    }
    return 1;
}
int selectAL(unsigned int *blk,Buffer *buf){
    printf("一趟扫描算法\n");
    int i,j,disk_Addr=100;
    for(i=0;i<16;++i){
        if((blk = readBlockFromDisk(i,buf))==NULL){
            perror("Reading Block Failed!\n");
            return 0 ;
        }
        for(j=0;j<7;++j){
            if(*(blk+2*j)==40){
                unsigned int *tmp_blk = getNewBlockInBuffer(buf);
                printf("R[%d][%d] = %d,%d\n",i,j,*(blk+2*j),*(blk+2*j+1));
                *tmp_blk = 40;
                *(tmp_blk+1) = *(blk+2*j+1);
                if (writeBlockToDisk(tmp_blk, disk_Addr, buf) != 0){
                    perror("Writing Block Failed!\n");
                    return 0;
                }
                disk_Addr++;
                freeBlockInBuffer(tmp_blk,buf);
            }
        }
        freeBlockInBuffer(blk,buf);
    }
    disk_Addr+=10;
    for(i=0;i<32;i++){
        if((blk = readBlockFromDisk(i+40,buf))==NULL){
            perror("Reading Block Failed!\n");
            return 0 ;
        }
        for(j=0;j<7;++j){
            if(*(blk+2*j+1)==69){
                unsigned int *tmp_blk = getNewBlockInBuffer(buf);
                printf("S[%d][%d] = %d,%d\n",i,j,*(blk+2*j),*(blk+2*j+1));
                *tmp_blk = *(blk+2*j);
                *(tmp_blk+1) = 69;
                if (writeBlockToDisk(tmp_blk, disk_Addr, buf) != 0){
                    perror("Writing Block Failed!\n");
                    return 0;
                }
                disk_Addr++;
                freeBlockInBuffer(tmp_blk,buf);
            }
        }
        freeBlockInBuffer(blk,buf);
    }
    return 1;
}
int store2(unsigned int* blk, Buffer* buf,int start0,int start1,int tag){
    int i,j,len,addr;
    addr = start1;
    if(tag == 0) len = 16;
    else len = 32;
    for(i=0;i<len;++i){
        if((blk = readBlockFromDisk(i+start0,buf))==NULL){
            perror("Reading Block Failed!\n");
            return 0;
        }
        for(j=0;j<7;++j){
            printf("%d ",*(blk+2*j));
            unsigned int *tmp_blk = getNewBlockInBuffer(buf);
            *tmp_blk = *(blk+2*j);
            if(writeBlockToDisk(tmp_blk,addr,buf)!=0){
                perror("Writing Block Failed!\n");
                return 0;
            }
            addr++;
            freeBlockInBuffer(tmp_blk,buf);
        }
        freeBlockInBuffer(blk,buf);
    }
    printf("\n");
    return (addr - start1);
}
int projectionAL(unsigned int* blk, Buffer* buf){
    /*对R.A进行投影
    * 复制    blk150 - blk261
    * 归并排序
    * 去重
    */
    printf("对R.A进行投影\n");
    int addr = 150;
    int i,j,off = 200;
    int num = store2(blk,buf,0,addr,0);
    printf("%d\n",num);
    //store2(blk,buf,40,1500,1);
    MergeSort(addr,num,buf);
    for(i=0;i<num;i++)
    {
        blk = readBlockFromDisk(addr+i,buf);
        printf("%d ",*blk);
        freeBlockInBuffer(blk,buf);
    }
    printf("\n");
    int s = split(addr,num,off,buf);
    printf("%d\n",s);
    printf("%d\n",addr+off);
    for(i=0;i<s;i++)
    {
        blk = readBlockFromDisk(addr+off+i,buf);
        printf("%d ",*blk);
        freeBlockInBuffer(blk,buf);
    }
    printf("\n");
    return 1;
}
int MergeSort(unsigned int addr, int n, Buffer* buf){
    if(n==1)
        return addr;
    unsigned int ll = MergeSort(addr,n/2,buf);
    unsigned int rr = MergeSort(addr+n/2,n-n/2,buf);
    return Merge(ll,n/2,rr,n-n/2,buf);
}
int Merge(unsigned int left,int lnum,unsigned int right,int rnum,Buffer *buf)
{
    int l=0,r=0;//计数
    int offset=0,i;
    unsigned int tmpaddr=left+500;  //结果存入的地址 650-761
    unsigned int *blk1,*blk2;
    while(l<lnum||r<rnum){
        if(l==lnum)                 //左边结束
            *blk1=1e5;
        else blk1=(int *)readBlockFromDisk(left+l,buf);
        if(r==rnum)
             *blk2=1e5;//右边结束
        else blk2=(int *)readBlockFromDisk(right+r,buf);
        if(*blk1<*blk2){
            writeBlockToDisk(blk1,tmpaddr+offset,buf);
            l++;
            offset++;
        }
        else{
            writeBlockToDisk(blk2,tmpaddr+offset,buf);
            r++;
            offset++;
        }
        freeBlockInBuffer(blk1,buf);
        freeBlockInBuffer(blk2,buf);
    }
    for(i=0;i<offset;i++)//写回
    {
        blk1=(int*)readBlockFromDisk(tmpaddr+i,buf);
        writeBlockToDisk(blk1,left+i,buf);
        freeBlockInBuffer(blk1,buf);
    }
    return left;
}

int split(unsigned int baseaddr,int num,int OFF, Buffer* buf){
    int count=1;
    blk=(int*)readBlockFromDisk(baseaddr,buf);
    unsigned int *disk_blk = getNewBlockInBuffer(buf);
    int tmp=*blk;
    *(disk_blk+OFF) = tmp;
    writeBlockToDisk(blk,baseaddr+OFF,buf);
    for(int i=1;i<num-1;++i){
        unsigned int *tmpblk=(int*)readBlockFromDisk(baseaddr+i,buf);
        if(tmp==*tmpblk){
            freeBlockInBuffer(tmpblk,buf);
            continue;
        }
        else{
            if(*tmpblk>tmp){
                writeBlockToDisk(tmpblk,baseaddr+OFF+count,buf);
                count++;
                tmp = *tmpblk;
                freeBlockInBuffer(tmpblk,buf);
            }
        }
    }
    return count;
}

int Nst_Loop_Join(unsigned int * blk,Buffer *buf){
    //800
    int si,sj,ri,rj;
    int A,B,C,D,num=0,addr = 800;
    for(si=0;si<32;++si){
        blk = readBlockFromDisk(si+40,buf);
        for(sj=0;sj<7;++sj){
            C= *(blk+2*sj);
            for(ri=0;ri<16;++ri){
                unsigned int * tmp_blk = readBlockFromDisk(ri,buf);
                for(rj=0;rj<7;++rj){
                    A = *(tmp_blk+2*rj);
                    if(A==C){
                        B = *(tmp_blk+2*rj+1);
                        D = *(blk+2*sj+1);
                        unsigned int *blk2 = getNewBlockInBuffer(buf);
                        *(blk) = A;
                        *(blk+1) = B;
                        *(blk+2) = C;
                        *(blk+3) = D;
                        writeBlockToDisk(blk2,addr+num,buf);
                        num++;
                        freeBlockInBuffer(blk2,buf);
                    }
                }
                freeBlockInBuffer(tmp_blk,buf);
            }
        }
        freeBlockInBuffer(blk,buf);
    }
    return num;
}

void connectionAL(unsigned int *blk,Buffer *buf){
    int ch;
    printf("==============1.NLJ 2.Merge 3.Hash -1.back===============\n");
    scanf("%d",&ch);
    switch(ch){
        case 1:{
            int num = Nst_Loop_Join(blk,buf);
            for(int i=0;i<num;++i){
                blk = readBlockFromDisk(800+i,buf);
                printf("R.A:%d R.B %d S.C %d S.D %d\n",*(blk),*(blk+1),*(blk+2),*(blk+3));
                freeBlockInBuffer(blk,buf);
            }
            break;
        }
        case 2:{

            break;
        }
        case 3:{
            break;
        }
        case -1:{
            return;
        }
        default:{
            printf("invalid value!!");
        }
    }
}
