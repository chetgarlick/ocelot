#include <SDL2/SDL.h>
#include <stdio.h>
#include <string>
#include <iostream>
#include <stdio.h>

//screen dimensions
const int WIDTH = 640;
const int HEIGHT = 480;

bool init();

int main(int argc, char* args[]) {

    printf("Running.");

    SDL_Window* window = NULL;

    SDL_Surface* surface = NULL;

    if ( SDL_Init( SDL_INIT_VIDEO ) < 0 ) {
        printf("Init error: %s\n", SDL_GetError() );
    } else {

        window = SDL_CreateWindow("Ocelot", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, WIDTH, HEIGHT, SDL_WINDOW_SHOWN);
        if(window == NULL){
			printf( "Window could not be created! SDL_Error: %s\n", SDL_GetError() );
        } else {
            			//Get window surface
			surface = SDL_GetWindowSurface( window );

			//Fill the surface white
			SDL_FillRect( surface, NULL, SDL_MapRGB( surface->format, 0xFF, 0xFF, 0xFF ) );
			
			//Update the surface
			SDL_UpdateWindowSurface( window );

			//Wait two seconds
			SDL_Delay( 2000 );
        }

    }
    
    //Destroy window
    SDL_DestroyWindow( window );

    SDL_Quit();

    return 0;
};