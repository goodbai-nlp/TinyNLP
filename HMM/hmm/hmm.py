#coding:UTF-8
import numpy as np

class HMM:
    def __init__(self, Ann, Bnm, pi1n):
        self.A = np.array(Ann)
        self.B = np.array(Bnm)
        self.pi = np.array(pi1n)
        self.N = self.A.shape[0]
        self.M = self.B.shape[1]

    def printhmm(self):
        print "HMM content: N =",self.N,",M =",self.M
        for i in range(self.N):
            if i==0:
                print "hmm.A ",self.A[i,:]," hmm.B ",self.B[i,:]
            else:
                print "      ",self.A[i,:],"       ",self.B[i,:]
        print "hmm.pi",self.pi

    # 前向算法估计参数
    # phmm:指向HMM的指针
    # T:观察值序列的长度 O:观察值序列
    # alpha:运算中用到的临时数组 pprob:返回值,所要求的概率
    def Forward(self,T,O,alpha,pprob):
    #   1. Initialization
        for i in range(self.N):
            alpha[0,i] = self.pi[i]*self.B[i,O[0]]
            print "alpha[0][%d] = pi[%d] * b[%d][%d] = %f *%f = %f"%(i,i,i,O[i],self.pi[i],self.B[i][O[0]],alpha[0][i])
    #   2. Induction
        for t in range(T-1):
            for j in range(self.N):
                sum = 0.0
                for i in range(self.N):
                    sum += alpha[t,i]*self.A[i,j]
                alpha[t+1,j] =sum*self.B[j,O[t+1]]
                print "alpha[%d][%d] = sum * b[%d][%d] = %f *%f = %f" % (t+1,
                j, j, O[t+1], sum, self.B[j][O[t+1]],alpha[t+1][j])
    #  3. Termination
        pprob[0] = 0.0
        for i in range(self.N):
            pprob[0] += alpha[T-1,i]
        print "pprob = ",pprob[0]
    #     带修正的前向算法
    def ForwardWithScale(self,T,O,alpha,scale,pprob):
        scale[0] = 0.0
    #     1. Initialization
        for i in range(self.N):
            alpha[0,i] = self.pi[i]*self.B[i,O[0]]
            scale[0] += alpha[0,i]

        for i in range(self.N):
            alpha[0,i] /= scale[0]

    #     2. Induction
        for t in range(T-1):
            scale[t+1] = 0.0
            for j in range(self.N):
                sum = 0.0
                for i in range(self.N):
                    sum += alpha[t,i]*self.A[i,j]

                alpha[t+1,j] = sum * self.B[j,O[t+1]]
                scale[t+1] += alpha[t+1,j]
            for j in range(self.N):
                alpha[t+1,j] /= scale[t+1]

    #     3. Termination
        pprob[0]=0.0
        for t in range(T):
            pprob[0] += np.log(scale[t])

    # 函数名称：Backward * 功能:后向算法估计参数 * 参数:phmm:指向HMM的指针
    # T:观察值序列的长度 O:观察值序列
    # beta:运算中用到的临时数组 pprob:返回值，所要求的概率
    def Backword(self,T,O,beta,pprob):
    #     1. Intialization
        for i in range(self.N):
            beta[T-1,i] = 1.0
    #     2. Induction
        for t in range(T-2,-1,-1):
            for i in range(self.N):
                sum = 0.0
                for j in range(self.N):
                    sum += self.A[i,j]*self.B[j,O[t+1]]*beta[t+1,j]
                beta[t,i] = sum

    #     3. Termination
        pprob[0] = 0.0
        for i in range(self.N):
            pprob[0] += self.pi[i]*self.B[i,O[0]]*beta[0,i]

    # 带修正的后向算法
    def BackwardWithScale(self,T,O,beta,scale):
    #     1. Intialization
        for i in range(self.N):
            beta[T-1,i] = 1.0

    #     2. Induction
        for t in range(T-2,-1,-1):
            for i in range(self.N):
                sum = 0.0
                for j in range(self.N):
                    sum += self.A[i,j]*self.B[j,O[t+1]]*beta[t+1,j]
                beta[t,i] = sum / scale[t+1]

    # Viterbi算法
    # 输入：A，B，pi,O 输出P(O|lambda)最大时Poptimal的路径I
    def viterbi(self,O):
        T = len(O)
        # 初始化
        delta = np.zeros((T,self.N),np.float)
        phi = np.zeros((T,self.N),np.float)
        I = np.zeros(T)
        for i in range(self.N):
            delta[0,i] = self.pi[i]*self.B[i,O[0]]
            phi[0,i] = 0
        # 递推
        for t in range(1,T):
            for i in range(self.N):
                delta[t,i] = self.B[i,O[t]]*np.array([delta[t-1,j]*self.A[j,i]  for j in range(self.N)]).max()
                phi[t,i] = np.array([delta[t-1,j]*self.A[j,i]  for j in range(self.N)]).argmax()
        # 终结
        prob = delta[T-1,:].max()
        I[T-1] = delta[T-1,:].argmax()
        # 状态序列求取
        for t in range(T-2,-1,-1):
            I[t] = phi[t+1,I[t+1]]
        return I,prob

    # 计算gamma : 时刻t时马尔可夫链处于状态Si的概率
    def ComputeGamma(self, T, alpha, beta, gamma):
        for t in range(T):
            denominator = 0.0
            for j in range(self.N):
                gamma[t,j] = alpha[t,j]*beta[t,j]
                denominator += gamma[t,j]
            for i in range(self.N):
                gamma[t,i] = gamma[t,i]/denominator

    # 计算sai(i,j) 为给定训练序列O和模型lambda时：
    # 时刻t是马尔可夫链处于Si状态，二时刻t+1处于Sj状态的概率
    def ComputeXi(self,T,O,alpha,beta,gamma,xi):
        for t in range(T-1):
            sum = 0.0
            for i in range(self.N):
                for j in range(self.N):
                    xi[t,i,j] = alpha[t,i]*beta[t+1,j]*self.A[i,j]*self.B[j,O[t+1]]
                    sum += xi[t,i,j]
            for i in range(self.N):
                for j in range(self.N):
                    xi[t,i,j] /= sum

    # Baum-Welch算法,非监督模型
    # 输入 L个观察序列O，初始模型：HMM={A,B,pi,N,M}
    def BaumWelch(self,L,T,O,alpha,beta,gamma):
        print "BaumWelch"
        DELTA = 0.01 ; round = 0 ; flag = 1 ; probf = [0.0]
        delta = 0.0 ; deltaprev = 0.0 ; probprev = 0.0 ; ratio = 0.0 ; deltaprev = 10e-70

        xi = np.zeros((T,self.N,self.N))
        pi = np.zeros((T),np.float)
        denominatorA = np.zeros((self.N),np.float)
        denominatorB = np.zeros((self.N),np.float)
        numeratorA = np.zeros((self.N,self.N),np.float)
        numeratorB = np.zeros((self.N,self.M),np.float)
        scale = np.zeros((T),np.float)

        while True :
            probf[0] = 0
            # E - step
            for l in range(L):
                self.ForwardWithScale(T,O[l],alpha,scale,probf)
                self.BackwardWithScale(T,O[l],beta,scale)
                self.ComputeGamma(T,alpha,beta,gamma)
                self.ComputeXi(T,O[l],alpha,beta,gamma,xi)
                for i in range(self.N):
                    pi[i] += gamma[0,i]
                    for t in range(T-1):
                        denominatorA[i] += gamma[t,i]
                        denominatorB[i] += gamma[t,i]
                    denominatorB[i] += gamma[T-1,i]

                    for j in range(self.N):
                        for t in range(T-1):
                            numeratorA[i,j] += xi[t,i,j]
                    for k in range(self.M):
                        for t in range(T):
                            if O[l][t] == k:
                                numeratorB[i,k] += gamma[t,i]

            # M - step
            # 重估状态转移矩阵 和 观察概率矩阵
            for i in range(self.N):
                self.pi[i] = 0.001/self.N + 0.999*pi[i]/L
                for j in range(self.N):
                    self.A[i,j] = 0.001/self.N + 0.999*numeratorA[i,j]/denominatorA[i]
                    numeratorA[i,j] = 0.0

                for k in range(self.M):
                    self.B[i,k] = 0.001/self.M + 0.999*numeratorB[i,k]/denominatorB[i]
                    numeratorB[i,k] = 0.0

                pi[i]=denominatorA[i]=denominatorB[i]=0.0

            if flag == 1:
                flag = 0
                probprev = probf[0]
                ratio = 1
                continue

            delta = probf[0] - probprev
            ratio = delta / deltaprev
            probprev = probf[0]
            deltaprev = delta
            round += 1

            if ratio <= DELTA :
                print "num iteration ",round
                break

def testForward():
    print "-------------------------TestForward----------------------------------"
    A = [
        [0.500, 0.375, 0.125],
        [0.250, 0.125, 0.625],
        [0.250, 0.375, 0.375]
    ]
    B = [
        [0.60, 0.20, 0.15, 0.05],
        [0.25, 0.25, 0.25, 0.25],
        [0.05, 0.10, 0.35, 0.50]
    ]
    pi = [0.63, 0.17, 0.20]
    hmm2 = HMM(A, B, pi)
    hmm2.printhmm()
    O = [0, 2, 3]
    T = 3
    alpha = np.zeros((T, hmm2.N), np.float)
    tmp = [0.0]
    hmm2.Forward(T, O, alpha, tmp)

def testViterbi():
    print "--------------------------TestViterbi------------------------------"
    A = [
        [0.333,0.333,0.333],
        [0.333,0.333,0.333],
        [0.333,0.333,0.333]
    ]
    B = [
        [0.5,0.5],
        [0.75,0.25],
        [0.25,0.75]
    ]
    Pi = [0.333,0.333,0.333]
    O = [0,0,0,0,1,0,1,1,1,1]
    hmm3 = HMM(A,B,Pi)
    hmm3.printhmm()
    I,prob=hmm3.viterbi(O)
    print "prob=",prob
    print I
def testBW():
    print "-----------------------------TestBaum-Welch------------------------"
    A = [[0.8125, 0.1875], [0.2, 0.8]]
    B = [[0.875, 0.125], [0.25, 0.75]]
    pi = [0.5, 0.5]
    hmm = HMM(A, B, pi)

    O = [[1, 0, 0, 1, 1, 0, 0, 0, 0],
         [1, 1, 0, 1, 0, 0, 1, 1, 0],
         [0, 0, 1, 1, 0, 0, 1, 1, 1]]
    L = len(O)
    T = len(O[0])
    alpha = np.zeros((T, hmm.N), np.float)
    beta = np.zeros((T, hmm.N), np.float)
    gamma = np.zeros((T, hmm.N), np.float)
    hmm.BaumWelch(L, T, O, alpha, beta, gamma)
    hmm.printhmm()

if __name__ == "__main__":
    print "python my HMM"
    testBW()
    testForward()
    testViterbi()

