#include<stdio.h>
#include<stdlib.h>
#include<time.h>

#define MAX_NUMBER 100

/* external variable */
int secret_number;

/* prototypes */
void initialize_number_generator(void);
void choose_new_secret_number(void);
void read_guesses(void);

char get_command(void){
    char command;
    printf("Play again? (Y/N)");
    if(!scanf(" %c", &command))
        exit(-2);
    return command;
}

int main (void)
{
    printf("Guess the secret number between 1 to %d.\n\n", MAX_NUMBER);
    initialize_number_generator();

    while(get_command()== 'y' || get_command() == 'Y'){
        choose_new_secret_number();
        printf("A secret number has been chosen.\n");
        read_guesses();
        printf("\n");
    }
    return 0;
}

void initialize_number_generator(void)
{
    srand((unsigned) time(NULL));
}

void choose_new_secret_number(void)
{
    secret_number = rand() % MAX_NUMBER + 1;
}

void read_guesses(void)
{
    int guess, num_guesses = 0;

    for(;;){
        num_guesses++;
        printf("Enter guess: ");
        if(!scanf("%d", &guess))
            exit(-1);
        if (guess == secret_number) {
            printf("You won in %d guesses!\n\n", num_guesses);
            //exit(0);
            return ;
        }
        else if (guess < secret_number) {
            printf("Too low; try anagin.\n");
        }
        else if (guess > secret_number) {
            printf("Too high; try anagin.\n");
        }
    }
}
