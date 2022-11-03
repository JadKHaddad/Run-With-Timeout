#include <time.h>
#include <unistd.h>
#include <pthread.h>
#include <stdio.h>
/* for ETIMEDOUT */
#include <errno.h>
#include <string.h>

typedef struct
{
        int bar;
        int baz;
} foo;

int run_with_timeout(void (*f)(void *in, void *out, int *err), void *in, void *out, int *err, struct timespec *max_wait)
{
        pthread_mutex_t calculating = PTHREAD_MUTEX_INITIALIZER;
        pthread_cond_t done = PTHREAD_COND_INITIALIZER;

        struct timespec abs_time;
        pthread_t tid;

        void *expensive_call(void *data)
        {
                /* ... calculations and expensive io here */
                f(in, out, err);

                /* wake up the caller if we've completed in time */
                pthread_cond_signal(&done);

                return NULL;
        }

        /* pthread cond_timedwait expects an absolute time to wait until */
        clock_gettime(CLOCK_REALTIME, &abs_time);
        abs_time.tv_sec += max_wait->tv_sec;
        abs_time.tv_nsec += max_wait->tv_nsec;

        pthread_create(&tid, NULL, expensive_call, NULL);

        /* pthread_cond_timedwait can return spuriously: this should
         * be in a loop for production code
         */
        return pthread_cond_timedwait(&done, &calculating, &abs_time);
}

void infinite_loop(void *in, void *out, int *err)
{
        while (1)
        {
                printf("infinite loop\n");
                sleep(1);
        }
}

int add(int a, int b)
{
        return a + b;
}

void scc(void *in, void *out, int *err)
{
        int *a = (int *)in;
        int *b = (int *)out;
        *b = add(*a, 1);
}

void fail(void *in, void *out, int *err)
{
        for (;;)
                ;
        int *a = (int *)in;
        int *b = (int *)out;
        *b = add(*a, 1);
}

void err(void *in, void *out, int *err)
{
        /* Lol */
        *err = -1;
}

void give_foo(void *in, void *out, int *err)
{
        foo *f = (foo *)out;
        f->bar = 1;
        f->baz = 2;
}

int main()
{
        struct timespec max_wait;
        memset(&max_wait, 0, sizeof(max_wait));
        max_wait.tv_sec = 2;

        int in = 1;
        int out = 0;
        if (run_with_timeout(scc, &in, &out, NULL, &max_wait) == ETIMEDOUT)
        {
                printf("timeout\n");
        }
        else
        {
                printf("res = %d\n", out);
        }

        in = 1;
        out = 0;
        if (run_with_timeout(fail, &in, &out, NULL, &max_wait) == ETIMEDOUT)
        {
                printf("timeout\n");
        }
        else
        {
                printf("res = %d\n", out);
        }

        foo f;
        if (run_with_timeout(give_foo, NULL, &f, NULL, &max_wait) == ETIMEDOUT)
        {
                printf("timeout\n");
        }
        else
        {
                printf("res = foo.bar [%d] | foo.baz [%d]\n", f.bar, f.baz);
        }

        int e = 0;
        if (run_with_timeout(err, NULL, NULL, &e, &max_wait) == ETIMEDOUT)
        {
                printf("timeout\n");
        }
        else
        {
                if (e == -1)
                {
                        printf("error\n");
                }
        }

        /* run_with_timeout will not terminate the task*/
        if (run_with_timeout(infinite_loop, NULL, NULL, NULL, &max_wait) == ETIMEDOUT)
        {
                printf("timeout\n");
        }

        sleep(10);
        return 0;
}
