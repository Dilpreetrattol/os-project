#include <windows.h>
#include <stdio.h>
#include <tchar.h>

#define PIPE_NAME _T("\\\\.\\pipe\\MessagePipe")

int main() {
    HANDLE hPipe;
    TCHAR buffer[1024];
    DWORD bytesRead;

    // Connect to the named pipe
    printf("Child: Connecting to the pipe...\n");
    hPipe = CreateFile(
        PIPE_NAME,                // Pipe name
        GENERIC_READ | GENERIC_WRITE, // Read/Write access
        0,                        // No sharing
        NULL,                     // Default security attributes
        OPEN_EXISTING,            // Opens existing pipe
        0,                        // Default attributes
        NULL                      // No template file
    );

    if (hPipe == INVALID_HANDLE_VALUE) {
        fprintf(stderr, "CreateFile failed. Error: %ld\n", GetLastError());
        return 1;
    }

    // Read the message from the pipe
    if (!ReadFile(hPipe, buffer, sizeof(buffer), &bytesRead, NULL)) {
        fprintf(stderr, "ReadFile failed. Error: %ld\n", GetLastError());
        CloseHandle(hPipe);
        return 1;
    }

    printf("Child: Message received: \"%s\"\n", buffer);

    // Clean up
    CloseHandle(hPipe);
    return 0;
}