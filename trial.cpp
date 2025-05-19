#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Clear screen for Windows
void clearScreen() {
    system("cls");  // Use "clear" for Linux/macOS
}

void showLinuxCommand(int cmd) {
    printf("\n------------------\n");
    switch(cmd) {
        case 1:
            printf("Internal vs External Commands:\n");
            printf("Internal: Built into shell (cd, pwd, echo)\n");
            printf("External: Separate executables (ls, grep, sort)\n");
            break;

        case 2:
            printf("Pipelining Commands:\n");
            printf("What it does: Sends output of one command as input to another\n");
            printf("How to use: command1 | command2\n");
            printf("Example: ls | sort\n");
            break;

        case 3:
            printf("Combining Commands:\n");
            printf("Semicolon (;): Run sequentially\n");
            printf("AND (&&): Run second if first succeeds\n");
            printf("Example: cd Documents && ls\n");
            break;

        case 4:
            printf("File Permissions:\n");
            printf("chmod: Change file permissions\n");
            printf("Example: chmod 755 file.txt\n");
            break;

        default:
            printf("Invalid Linux command choice!\n");
    }
    printf("------------------\n");
}

void showThreadConcept(int cmd) {
    printf("\n------------------\n");
    switch(cmd) {
        case 1:
            printf("User-Level Threads:\n");
            printf("- Managed by user-level libraries.\n");
            printf("- Fast context switching.\n");
            printf("- Kernel is unaware of threads.\n");
            break;

        case 2:
            printf("Kernel-Level Threads:\n");
            printf("- Managed by the OS kernel.\n");
            printf("- More overhead but better system integration.\n");
            printf("- Each thread is treated independently by the OS.\n");
            break;

        case 3:
            printf("User vs Kernel Threads:\n");
            printf("- User threads are faster but can't take advantage of multi-core.\n");
            printf("- Kernel threads are slower but offer better concurrency.\n");
            printf("- Many-to-One, One-to-One, Many-to-Many models exist.\n");
            break;

        default:
            printf("Invalid thread concept choice!\n");
    }
    printf("------------------\n");
}

int getUserChoice(int min, int max) {
    char input[100];
    int choice;
    fgets(input, sizeof(input), stdin);
    if (sscanf(input, "%d", &choice) != 1 || choice < min || choice > max) {
        return -1;  // invalid input
    }
    return choice;
}

int main() {
    int mainChoice, subChoice;

    while (1) {
        clearScreen();
        printf("===== Explore Topics =====\n");
        printf("1. Linux Commands\n");
        printf("2. Thread Concepts\n");
        printf("0. Exit\n");
        printf("==========================\n");
        printf("Choose a topic: ");

        mainChoice = getUserChoice(0, 2);

        if (mainChoice == -1) {
            printf("Invalid input! Press Enter to try again...");
            getchar();
            continue;
        }

        if (mainChoice == 0) {
            printf("Goodbye!\n");
            break;
        }

        clearScreen();

        if (mainChoice == 1) {
            printf("== Linux Commands ==\n");
            printf("1. Internal vs External\n");
            printf("2. Pipelining (|)\n");
            printf("3. Combining Commands (;, &&)\n");
            printf("4. File Permissions (chmod)\n");
            printf("0. Back\n");
            printf("====================\n");
            printf("Choose a command to learn: ");
            subChoice = getUserChoice(0, 4);

            if (subChoice == 0) continue;

            clearScreen();
            showLinuxCommand(subChoice);
        }

        else if (mainChoice == 2) {
            printf("== Thread Concepts ==\n");
            printf("1. User-level Threads\n");
            printf("2. Kernel-level Threads\n");
            printf("3. Differences\n");
            printf("0. Back\n");
            printf("======================\n");
            printf("Choose a thread concept: ");
            subChoice = getUserChoice(0, 3);

            if (subChoice == 0) continue;

            clearScreen();
            showThreadConcept(subChoice);
        }

        printf("\nPress Enter to return to main menu...");
        getchar();
    }

    return 0;
}
