#include <SDL2/SDL.h>
#include <stdio.h>
#include <string>
#include <iostream>
#include <stdio.h>

//screen dimensions
const int WIDTH = 640;
const int HEIGHT = 480;

bool init();

bool loadMedia();

void close();

SDL_Window* window = NULL;

SDL_Surface* surface = NULL;

bool init(){
    bool success = true;

    //Initialize SDL
	if( SDL_Init( SDL_INIT_VIDEO ) < 0 )
	{
		printf( "SDL could not initialize! SDL_Error: %s\n", SDL_GetError() );
		success = false;
	} else {
		//Create window
		window = SDL_CreateWindow( "SDL Tutorial", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, WIDTH, HEIGHT, SDL_WINDOW_SHOWN );
		if( window == NULL )
		{
			printf( "Window could not be created! SDL_Error: %s\n", SDL_GetError() );
			success = false;
		}
		else
		{
			//Get window surface
			surface = SDL_GetWindowSurface( window );
		}
	}

    return success;
}

void close(){
    SDL_FreeSurface(surface);
    SDL_DestroyWindow(window);

    SDL_Quit();
}

int main(int argc, char* args[]) {

    printf("Running.\n");

    if ( !init() ){
        printf("Initialization failed.\n");
    } else {

        bool quit = false;

        SDL_Event e;

        while(!quit){

            while( SDL_PollEvent( &e )!= 0 ){
                if(e.type == SDL_QUIT){
                    quit = true;
                }
            }

			//Apply the image
			//SDL_BlitSurface( gXOut, NULL, gScreenSurface, NULL );
			
			//Update the surface
			//SDL_UpdateWindowSurface( gWindow );
        }
    }
    close();

    return 0;
};