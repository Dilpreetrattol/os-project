#include <stdio.h>
#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>

#define NUM_ITERATIONS 5

int shared_counter = 0;
sem_t semaphore;

void* thread_function(void* arg) {
    char* thread_name = (char*)arg;

    for (int i = 0; i < NUM_ITERATIONS; i++) {
        sem_wait(&semaphore); // Enter critical section

        // Critical Section
        int temp = shared_counter;
        printf("%s read shared_counter = %d\n", thread_name, temp);
        temp++;
        sleep(1); // simulate some processing delay
        shared_counter = temp;
        printf("%s updated shared_counter to %d\n", thread_name, shared_counter);

        sem_post(&semaphore); // Exit critical section
        sleep(1); // simulate some work outside critical section
    }

    pthread_exit(NULL);
}

int main() {
    pthread_t thread1, thread2;

    // Initialize semaphore with value 1 (like a mutex)
    sem_init(&semaphore, 0, 1);

    // Create threads
    pthread_create(&thread1, NULL, thread_function, "Thread 1");
    pthread_create(&thread2, NULL, thread_function, "Thread 2");

    // Wait for threads to finish
    pthread_join(thread1, NULL);
    pthread_join(thread2, NULL);

    printf("Final value of shared_counter = %d\n", shared_counter);

    // Destroy the semaphore
    sem_destroy(&semaphore);

    return 0;
}