/*-----------------------------------------
  linescape.cpp
  Written by Camille Utterback 
  August 2002
	camille@camilleutterback.com
	www.camilleutterback.com
  WHAT:

	This program moves and connects 3 dots.   
	Each of the 3 dots animates around it's own rectangle.

	The 3 dots are connected in their current location by a translucent white triangle.

	My program keeps track of former dot locations, and draws blue triangles connecting 
	the 3 dots in places they used to be.

	Like most (all?) things, the traces of where the dots have been fade over time.
	
	You can change the rectangles, 

		and therefore the trajectories of the dots,

			and therefore the patterns created over time, 

	by clicking anywhere on the screen.

	A random corner of one of the 3 rectangles will relocate to the spot you clicked.

	The dot controlled by that rectangle will move back onto it's trajectory around the
	new triangle (most of the time - sometimes it doesn't quite get back 'on track' but
	that was a mistake I liked so I left it.)

	To quit the program, hit ENTER on your keyboard.


  WHY:

	  This was apparently a very simple assignment: 'move and connect 3 dots'.

	  But all motion implies time. 

	  Time and motion can create complexity out of very simple things.
  
	  This is especially the case when a simple shape (a triangle) repeated over
	  and over again, following another simple shape (a rectangle) creates a complicated 
	  network of lines. 

	  Maybe it's simple math, but it fascinates me to watch curves emerge from the 
	  accumulation of straight lines.

	  And I know it's all 0's and 1's but sometimes it's hard to believe the garbledeegook
	  of code I write is a system of simple rules from which I can create endless variation
	  and complexity.

	  Computers are not necessary to experience the emergence of something complicated out
	  of simple rules, they just make it faster.

	  (After completing this program I realized it is was an inadvertent homage to string art 
	  from my childhood.)

  CODE NOTES:

	  This code works on Windows98, Windows 2000, and Windows XP machines 
	  with graphics cards that support OpenGL.

	  I've arranged the code so that my main functions are in one section
	  titled 'My Functions' and the functions that allow this program to interact 
	  with the Windows operating system are in a section titled 'Windows Main and Windows
	  Management Functions'

	  I was a bit embarrassed and nervous to think of people looking at my code, so I've 
	  taken out a lot of my comments where I'm cursing, venting my frustration and thoughts
	  and keeping track of what I've tried and not. In retrospect maybe this was a mistake, 
	  as this code no longer really looks like what a working file of mine looks like.
	  What can I say? I'm one of those people that clean my bathroom if my friends are coming over.
--------------------------------------------------*/
//---------------------------------------------------------------------------------------
//---------------------------------INCLUDES/DEFINES
//---------------------------------------------------------------------------------------

#include <windows.h> 
#include <gl/glut.h>	//uses glut, guarantees gl.h and glu.h are properly included 

#include <time.h>	 

#define MAXTRAILPOINTS 500  



//---------------------------------------------------------------------------------------

//---------------------------------FUNCTIONS

//---------------------------------------------------------------------------------------

//---Windows Management Functions

LRESULT CALLBACK WindowProc(HWND, UINT, WPARAM, LPARAM);


//---My General Setup and Cleanup Functions

void MySetUp(HWND passedhwnd); 

	bool CreateCurrentGLContext(HGLRC whichglrc,HDC whichdc,int width,int height);
	void SetupOpenGLParams();


void CleanUp();


//---My Drawing Functions and Functions they rely on

void MyMainFunction();

	void MoveConnectAndDrawStuff();

		void IncrementPointToTarget(POINT *ppoint, int *ptarget, int targetdir, int speed, RECT rect);
		void IncrementTrailPtPtr();

void MyMouseDownFunction(int mouseX,int mouseY);



//---------------------------------------------------------------------------------------

//---------------------------------VARIABLES

//---------------------------------------------------------------------------------------


//-------------GENERAL

int ScreenX, ScreenY;	//screen dimensions

clock_t LastClockTime;	



//-------------WINDOW/OBJECTS

HWND hwnd;	//main window

HDC hdc;	//screen device context

HGLRC hglrc; //opengl rendering context, uses a dc to draw on



//-------------DRAWING VARIABLES


POINT dot[3];			//-- array of 3 points

RECT tracerect[3];		//-- array of 3 rectangles
						//each dot animates around one of these 'tracerects'

int targetcorner[3];	//-- array of 3 numbers	
						//this stores the target corner 
						//that each point is animating towards in its respective 'tracerect'
						//initially, 0 is the top left, 1 the top right, 2 the bottom right, 3 the bottom left.
						//but since clicking can reorient the rectangle I pick numbers for the corners 
						//instead of referring to them as top right etc.
	
int dotdirection[3]={	1,	//dot 0
			1,	//dot 1
			-1	//dot 2
			};
				
						//--dot direction controls whether dots are moving from targe corner 0-1-2 etc, or 3-2-1 etc.
	
	
int dotspeed[3]=	{	20,		//dot 0
				3,		//dot 1
				15		//dot 2
			};

						//--dot speed controls how many pixels a dot moves each 



GLfloat TrailPtList[3][MAXTRAILPOINTS*3];	//3 lists - one for each dot
												//each list stores the location (x,y) and alpha value 
												//of each dot over time, up to MAXTRAILPOINTS

int TrailPtPtr=0;				//pointer to next available space in TrailLists
												//the lists are filled consistently, so one pointer will do





//I could have made all this a struct - oh well!




//---------------------------------------------------------------------------------------

//---------------------------------MY FUNCTIONS

//---------------------------------------------------------------------------------------



void MyMainFunction(){

	if((clock()-LastClockTime)>(CLOCKS_PER_SEC/30)){ //test if enough time has gone by

		glClear(GL_COLOR_BUFFER_BIT);		//clear screen buffer to bkgd color

		MoveConnectAndDrawStuff();		//this is the 'move and connect 3 dots' part

		glFlush();				//force drawing to finish

		SwapBuffers(hdc);			//move drawing to screen

		LastClockTime=clock();			//store the current time
	}


}//end MyMainFunction 


//-----------------------------



void MyMouseDownFunction(int mouseX,int mouseY){ 

int whichrect;

		//--adjust the mousey for OpenGL coords

		mouseY=ScreenY-mouseY; 
									

		//--reset a random corner of a random trace rect to the mouse position

		whichrect=rand()%3;	//pick a random number 0,1,or 2 
		

		switch(rand()%4){

		case 0:
			tracerect[whichrect].left=mouseX;
			tracerect[whichrect].top=mouseY;
			break;
		case 1:
			tracerect[whichrect].right=mouseX;
			tracerect[whichrect].top=mouseY;
			break;
		case 2:
			tracerect[whichrect].right=mouseX;
			tracerect[whichrect].bottom=mouseY;
			break;
		case 3:
			tracerect[whichrect].left=mouseX;
			tracerect[whichrect].bottom=mouseY;
			break;
		}


		//--reset the speed for this rect to a random number between 3 and 20

		dotspeed[whichrect] = rand()%20+3;


}//end MyMouseDownFunction 

//------------------------------



void MoveConnectAndDrawStuff(){


//This function does all kinds of stuff, 
	//i.e. move, connect, and draw the dots
	//please see the numbered headings for details


//this function calls:
		//IncrementPointToTarget
		//IncrementTrailPtPtr




//1. MOVE DOT LOCATIONS AROUND 'TRACE RECTS'
	
	//--move all 3 dot locations around their respective 'trace rects'

	IncrementPointToTarget(&dot[0], &targetcorner[0], dotdirection[0], dotspeed[0], tracerect[0]);
	IncrementPointToTarget(&dot[1], &targetcorner[1], dotdirection[1], dotspeed[1], tracerect[1]);
	IncrementPointToTarget(&dot[2], &targetcorner[2], dotdirection[2], dotspeed[2], tracerect[2]);



	
//2. FADE OLD DOT'S ALPHA VALUES AND ADD NEW DOTS TO TRAIL LISTS

	//a. --loop through all trail points and decrease alpha values for every point- ie fade them

	int i,j;

	GLfloat faderate= 0.005;

	for(i=0;i<3;i++){

		for(j=0;j<MAXTRAILPOINTS;j++){

			TrailPtList[i][j*3+2]=max(0.0,TrailPtList[i][j*3+2]-faderate );
			TrailPtList[i][j*3+2]=max(0.0,TrailPtList[i][j*3+2]-faderate );
			TrailPtList[i][j*3+2]=max(0.0,TrailPtList[i][j*3+2]-faderate );

		}//end j loop

	}//end i loop



	//b. --add the new dots to their trailpoint list and set that alpha to 1.0

	for(i=0;i<3;i++){

		for(j=0;j<MAXTRAILPOINTS;j++){

			TrailPtList[i][TrailPtPtr*3]=dot[i].x;		//set dot x loc
			TrailPtList[i][TrailPtPtr*3+1]=dot[i].y;		//set dot y loc
			TrailPtList[i][TrailPtPtr*3+2]=1.0;			//set alpha value

		}//end j loop

	}//end i loop



	//c. --increment trail point list pointer to next available storage index in the arrays

	IncrementTrailPtPtr(); 
	
	//This function increments TrailPtPtr and shifts active index points up the array if TrailPtPtr is at the end of the arrays




//3. PRINT - DRAW LINES BETWEEN ALL THE DOTS (former dot locations) IN TRAIL LISTS



	glBegin(GL_LINE_STRIP);
		
		for(j=0;j<MAXTRAILPOINTS;j++){ 

			if(TrailPtList[0][j*3+2]>0.0){ //if the point has not faded to 0.0

					for(i=0;i<3;i++){

						//connect one dot from each list to form a triangle

						glColor4f(0.5, 0.5, 1.0, TrailPtList[i][j*3+2]);	//use stored alpha value
						glVertex2i(TrailPtList[i][j*3],TrailPtList[i][j*3+1]);

					}

			}//end if

		}//end maxtrailpoints loop
		
	glEnd();




//4. PRINT - DRAW THE 'TRACE RECTS' THAT DOTS ARE MOVING AROUND


	glColor4f(0.5, 0.5, 1.0, 1.0);	//set color and alpha

	for(i=0;i<3;i++){

		glBegin(GL_LINE_LOOP);

			glVertex2i(tracerect[i].left,tracerect[i].top);
			glVertex2i(tracerect[i].right,tracerect[i].top);
			glVertex2i(tracerect[i].right,tracerect[i].bottom);
			glVertex2i(tracerect[i].left,tracerect[i].bottom);
			
		glEnd();

	}//end tracerect loop




//5. PRINT --DRAW A TRANSPARENT WHITE TRIANGLE CONNECTING THE CURRENT 3 DOTS

	
	glColor4f(1.0, 1.0, 1.0, 0.75); 

	glBegin(GL_POLYGON);

		glVertex2i(dot[0].x,dot[0].y);
		glVertex2i(dot[1].x,dot[1].y);
		glVertex2i(dot[2].x,dot[2].y);
			
	glEnd();




}//end MoveConnectAndDrawStuff 



//-----------------------------



void IncrementPointToTarget(POINT *ppoint, int *ptarget, int targetdir, int speed, RECT rect){


//This function moves a point passed to it towards a target corner in the passed in rect structure
//The amount of motion is determined by the passed speed var
//If the new point location overshoots the target corner loc, then the point is reset to the corner loc
//and a new target corner is set based on the targetdir (some points move from corner 0 to 1 to 2, other from 2 to 1 to 0 etc.)

POINT corner[4];

corner[0].x = rect.left;
corner[0].y = rect.top;

corner[1].x = rect.right;
corner[1].y = rect.top;

corner[2].x = rect.right;
corner[2].y = rect.bottom;

corner[3].x = rect.left;
corner[3].y = rect.bottom;


//these coords may no longer BE at the top, bottom etc if rect has been moved
//ptarget is the _number_ of the corner the point is aiming for though.


int xdir, ydir; 



	//--figure out the x dir point needs to travel based on point and targetcorner
	if(corner[*ptarget].x - ppoint->x < 0) xdir=-1; 
	if(corner[*ptarget].x - ppoint->x > 0) xdir=1;
	if(corner[*ptarget].x - ppoint->x == 0) xdir=0;  

	//--figure out y dir point needs to travel based on point and targetcorner
	if(corner[*ptarget].y - ppoint->y < 0) ydir=-1; 
	if(corner[*ptarget].y - ppoint->y > 0) ydir=1;
	if(corner[*ptarget].y - ppoint->y == 0) ydir=0; 

	//--set new point location based on dot's speed and the direction calculated above
	ppoint->x=ppoint->x+xdir*speed;
	ppoint->y=ppoint->y+ydir*speed;



	if(	(ydir==1 && ppoint->y >= corner[*ptarget].y) || (ydir<0 && ppoint->y <= corner[*ptarget].y)){ 

		//dot is equal to or beyond it's target vertically (relative to the direction dot was moving)

			ppoint->y=corner[*ptarget].y;		//set y to the target corner y (in case we overshot)


			if(targetdir==1){

				*ptarget=(*ptarget+1<=3)?*ptarget+1:*ptarget=0; //increment target corner

			}else{

				*ptarget=(*ptarget-1>=0)?*ptarget-1:*ptarget=3; //decrement target corner
			}



	}else{

		if((xdir==1 && ppoint->x>=corner[*ptarget].x) || (xdir<0 && ppoint->x<=corner[*ptarget].x)){

			//dot is equal to or beyond it's target horizontally (relative to the direction dot was moving)
		
			ppoint->x=corner[*ptarget].x;		//set x to the target corner x (in case we overshot)


			if(targetdir==1){

				*ptarget=(*ptarget+1<=3)?*ptarget+1:*ptarget=0; //increment target corner

			}else{

				*ptarget=(*ptarget-1>=0)?*ptarget-1:*ptarget=3; //decrement target corner
			}

		}
	}



}//end IncrementPointToTarget

//---------------

void IncrementTrailPtPtr(){

	
	//--This function tries to increment TrailPtPtr, 
	//--(which keeps track of where to add new dot locations into the TrailPointLists)
	//--but first checks if TrailPtPtr is at the end of the array, 
	//--If it is, the function shifts all the active (not completely faded) points 
	//--back to the start of the array to make space at the end and sets TrailPtPtr accordingly

	//--(Shifting all the points seems dorky, but if I pass a 'wraped around' array to an openGL 
	//--draw function I got a 'seam' between the begining and end of the active points that didn't look good.
	//--this was the simplest way I thought of to solve it.)


	int shiftindex;
	int i,j,k;

	if(TrailPtPtr+1<MAXTRAILPOINTS){
		
		//--not at end of array, increment normally

		TrailPtPtr++; 

	}else{

		//--at the end of our array - shift active array elements back towards 0 index

		//find first active index pt. (point who's alpha is > 0.0)

		for(j=0;j<MAXTRAILPOINTS;j++){

			if(TrailPtList[0][j*3+2]>0.0) break;
		}

		//j should now be the first index who's value is over 0.0

		shiftindex=j;

		
		//move all index points up shiftindex places towards index 0

		for(k=0;k<MAXTRAILPOINTS;k++){ //loop through all the array points
				
				if(j<MAXTRAILPOINTS){ 
					// if j (which started at shiftindex) is still less than our original array

					for(i=0;i<3;i++){ //for each of our 3 arrays
						
						//shift the point at this index as far towards the begining of the array as possible

						TrailPtList[i][k*3]=TrailPtList[i][j*3];
						TrailPtList[i][k*3+1]=TrailPtList[i][j*3+1];
						TrailPtList[i][k*3+2]=TrailPtList[i][j*3+2];

					}//end i loop - once for each list

					j++;

				}else{

					//all the old active values have been shifted up

					for(i=0;i<3;i++){
						TrailPtList[i][k*3+2]=0.0; //reset the rest of each array to 0.0
					}

				}//end if j < MAXTRAILPOINTS

			}//end shift loop - looping through individual lists

		
		TrailPtPtr=TrailPtPtr-shiftindex+1; //move pointer 1 past end of newly shifted list
		
	}



}//end IncrementTrailPtPtr 

//---------------



void MySetUp(HWND passedhwnd){

	//this function calls
		//CreateCurrentGLContext
		//SetupOpenGLParams

int i,j;
	
		//-------------GET A HANDLE TO A DEVICE CONTEXT

		hdc=GetDC(passedhwnd);	//get a handle to the screen


			
		//-------------CREATE OPENGL RENDERING CONTEXT

		//this should be an IF, if it doesn't return a 1, program should quit 
		//oh well.

		CreateCurrentGLContext(hglrc,hdc,ScreenX,ScreenY);

		//creates an openGLContext and sets it's viewport to the screen size
		//also sets a 2D orthographic projection mode to screen size


		//-------------SET INITIAL VALUES FOR OPENGL PARAMS

		SetupOpenGLParams();



		//------------INITIALIZE TRACE RECTS

		int ctrX, ctrY;

		ctrX=ScreenX/2;
		ctrY=ScreenY/2;


		//--rect 0
		tracerect[0].left=	ctrX-100;		
		tracerect[0].top=	ctrY+20;	
		tracerect[0].right=	tracerect[0].left+ 250;		//width				
		tracerect[0].bottom=tracerect[0].top - 100;		//height
		

		//--rect 1 - upper right
		tracerect[1].left=	ctrX-200;	
		tracerect[1].top=	ctrY+200;			
		tracerect[1].right=	tracerect[1].left+ 100;		//width		
		tracerect[1].bottom=tracerect[1].top - 100;		//height


		//--rect 2 - long thin
		tracerect[2].left=	ctrX-20;		
		tracerect[2].top=	ctrY+250;				
		tracerect[2].right=	tracerect[2].left+ 50;		//width			
		tracerect[2].bottom=tracerect[2].top - 500;		//height



		//-------------INITIALIZE DOTS

		for(i=0;i<3;i++){

			//--start each dot in the ctr. of it's tracerect

			dot[i].x = tracerect[i].left+(tracerect[i].right-tracerect[i].left)/2;
			dot[i].y = tracerect[i].bottom+(tracerect[i].top-tracerect[i].bottom)/2;

			//--assign it a random target corner
			targetcorner[i]=rand()%3;

		}


		//-------------INITIALIZE TRAILPOINTLISTS

		//--set all the locations and alpha values of the 3 trailpoint lists to 0.0

		
		for(i=0;i<3;i++){
			for(j=0;j<3*MAXTRAILPOINTS;j+=3){

				TrailPtList[i][j]=0.0;
				TrailPtList[i][j+1]=0.0;
				TrailPtList[i][j+2]=0.0;
	
			}
		}
		


		//-------------STORE THE CURRENT TIME

		LastClockTime=clock();



}//end MySetUp

//------------------



void CleanUp(){
	//--------cleanup openGL rendering context
    if(hglrc = wglGetCurrentContext()) { 
		//if the thread has a rendering context:
        // make the rendering context not current 
        wglMakeCurrent(NULL, NULL); 
        // delete the OpenGL rendering context 
        wglDeleteContext(hglrc); 
        }
	//-------clean up GDI stuff
		DeleteDC(hdc); //release the screen device context
}//--end CleanUp function
//------------------------------
bool CreateCurrentGLContext(HGLRC whichglrc,HDC whichdc,int width,int height){

//This function creates an OpenGL rendering context using the buffers passed to it
//and sets the rendering context's viewport and an Ortho2Dprojection mode 
//based on the height and width passed in
	bool breturnflag=0;
	int  iPixelFormat; 
	//--setup the desired pixelformat structure
	PIXELFORMATDESCRIPTOR pfd = { 
				sizeof(PIXELFORMATDESCRIPTOR),		// size of this pfd 
				1,									// version number 
				//--dwFlags 
				PFD_DRAW_TO_WINDOW |   //The buffer can draw to a window or device surface
				PFD_SUPPORT_OPENGL|   // The buffer supports OpenGL drawing.
				PFD_DOUBLEBUFFER|      //The buffer is double-buffered. 
				//--ipixeltype
				PFD_TYPE_RGBA,         // iPixelType RGBA or index 
				24,                    // cColorBits - 
										//Specifies the number of color bitplanes in each color buffer. 
										//For RGBA pixel types, it is the size of the color buffer, excluding the alpha bitplanes.
										//24-bit color depth 

										//--color bits - ignored 
				8,						//cRedBits -the number of red bitplanes in each RGBA color buffer. 
				0,						//cRedShift - the shift count for red bitplanes in each RGBA color buffer. 
				8, 0,					//cBlueBits, cBlueShift
				8, 0,					//cGreenBits, cGreenShift

				0, 0,					//AlphaBits, AlphaShift
										//Specifies the number of alpha bitplanes in each RGBA color buffer. 
										//in generic gdi imp. Alpha bitplanes are not supported. 
				
				0,                     //cAccumBits - the total number of bitplanes in the accumulation buffer. 
				0, 0, 0, 0,            //cAccumRedBits, Green, Blue, Alpha

				0,						//cDepthBits - the depth of the depth (z-axis) buffer. 
										//was 32

				0,                     //cStencilBits - the depth of the stencil buffer.
										//8 is the max it will give me so far

				0,                     //cAuxBuffers - the number of auxiliary buffers. 
										//in generic gdi imp. Auxiliary buffers are not supported. 
 
				PFD_MAIN_PLANE,        //iLayerType - Ignored. older implementations used this

				0,                     //bReserved - the number of overlay and underlay planes. 
										//Bits 0 through 3 specify up to 15 overlay planes 
										//and bits 4 through 7 specify up to 15 underlay planes. 

				0,						//dwLayerMask -Ignored. older implementations used this

				0,						//dwVisibleMask - the transparent color or index of an underlay plane. 
										//When the pixel type is RGBA, dwVisibleMask is a transparent RGB color value. 
										//When the pixel type is color index, it is a transparent index value. 

				0						//dwDamageMask -Ignored. older implementations used this
			}; 
	//--- set the pixel format based on the pixelformat we setup above
			//--try to find a PIXELFORMATDESCRIPTOR with the specified attribs.
				//ChoosePixelFormat gets the best available match of pixel format for the device context  
			iPixelFormat = ChoosePixelFormat(whichdc, &pfd); 
			//--make that the pixel format of the device context 
			SetPixelFormat(whichdc, iPixelFormat, &pfd);
	//--- Create an OpenGL rendering context and set it's viewport and projection mode based on params passed to this function
			if (whichglrc = wglCreateContext(whichdc) ) { 
				//--create a rendering context using the device context passed to this function
				if(wglMakeCurrent(whichdc, whichglrc)){
					//--make this rendering context the thread's current rendering context 
					breturnflag=1; //rendering context was created and selected OK
					//--Set the OpenGL viewport to match the screen size
					glViewport(	0,					//The lower-left corner of the viewport rectangle, in pixels. The default is (0,0). 
								0,
								(GLsizei) width,	//The width and height, respectively, of the viewport.
								(GLsizei) height
								);
					//--set and load the matrix mode
					glMatrixMode(GL_PROJECTION); //Applies subsequent matrix operations to the specified matrix stack. 
					glLoadIdentity(); //replaces current matrix with the base matrix
					//--set the projection mode
					gluOrtho2D(		0.0, //The coordinates for the left and right vertical clipping planes. 
									(GLdouble) width, 
									0.0, //The coordinates for the bottom and top horizontal clipping planes. 
									(GLdouble) height
								);
				}//end if context made current 
			}//end if context created OK
	return breturnflag;
}
void SetupOpenGLParams(){
		//--------SET clearing/bkgd color
		//glClearColor(0.0, 0.0, 0.0, 0.0);//black
		glClearColor(1.0, 1.0, 1.0, 1.0); //white
		//--------SET INITIAL LINE SIZES
		glLineWidth(1.0);
		//--------SET SHADING OPTIONS
		glShadeModel(GL_FLAT); 
		//-------DEPTH
		glDisable(GL_DEPTH_TEST); 
		//-------LIGHTING
		glDisable(GL_LIGHTING);
		//-------BLENDING OPTIONS
		glEnable(GL_BLEND);
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA); 
}// end SetupOpenGLParams
//---------------------------------------------------------------------------------------
//------------------------WINDOWS MAIN 
//------------------------AND 
//------------------------WINDOWS MANAGEMENT FUNCTIONS
//---------------------------------------------------------------------------------------
int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInst, PSTR szCmdLine, int iCmdShow){
	static char szAppName[] = "dotodot";		//my application name
	MSG msg;									//var to hold Windows messages
	WNDCLASSEX wndclass;						//var to hold my application window parameters

	//------DEFINE AND REGISTER A WINDOW CLASS
	wndclass.cbSize = sizeof(wndclass);
	wndclass.style = 0;									//default style
	wndclass.hInstance = hInstance;						//handle to this instance
	wndclass.lpszClassName = szAppName;					//window class name
	wndclass.lpfnWndProc = WindowProc;					//window function
	wndclass.hIcon = LoadIcon(NULL, IDI_APPLICATION);	//icon style
	wndclass.hIconSm = LoadIcon(NULL, IDI_APPLICATION);
	wndclass.hCursor = LoadCursor(NULL, IDC_ARROW);		//cursor style
	wndclass.lpszMenuName = NULL;						//no menu
	wndclass.cbClsExtra = 0;							//no extra
	wndclass.cbWndExtra = 0;							//info needed
	wndclass.hbrBackground =(HBRUSH) GetStockObject(WHITE_BRUSH);
	RegisterClassEx (&wndclass);
	//------GET SCREEN DIMENSIONS
	ScreenX=GetSystemMetrics(SM_CXSCREEN);	//get the x dimension of the screen
	ScreenY=GetSystemMetrics(SM_CYSCREEN);	//get the y dimension of the screen	
	//------CREATE THE WINDOW
	hwnd = CreateWindow(
		szAppName,	//name of window class
		NULL,		//title 
		WS_POPUP,	//window style 
		0,			//x coordinate 
		0,			//y coordinate 
		ScreenX,	//width
		ScreenY,	//height
		NULL,		//no parent window
		NULL,		//menu handle (if parent) - child id if window is a child
		hInstance,	//handle of this instance of the program
		NULL		//no additional arguments
		);
		//note: windows sends a WM_CREATE msg to WindowProc while processing createwindow 
	//------DISPLAY WINDOW
	ShowWindow(hwnd, iCmdShow); //windows sends WM_SIZE, WM_SHOWWINDOW msg to WindowProc
	//------MAIN LOOP
	while (TRUE)
	{
		MyMainFunction();
		//--deal with messages windows is passing to my program
		if (PeekMessage (&msg, NULL, 0,0, PM_REMOVE))
		{
			if (msg.message == WM_QUIT)
				break;
			TranslateMessage(&msg);
			DispatchMessage(&msg);		
		}
	}//end while true
	return msg.wParam;
} //end Windows Main
LRESULT CALLBACK WindowProc(HWND hwnd, UINT iMsg, WPARAM wParam, LPARAM lParam)
{
//This function handles messages from the Operating System Message Queue
	switch(iMsg) 
	{
	case WM_CREATE:
		//--The Application Window was just created - Call My SetUp Function
		MySetUp(hwnd);
		return 0;
	case WM_LBUTTONDOWN:
		//--User just clicked the left mouse button - Call My MouseDown Function
		MyMouseDownFunction(LOWORD(lParam),HIWORD(lParam)); //pass it the x and y loc of the mouse
		return 0;
	case WM_KEYDOWN:
		switch(wParam)
		{
			case VK_RETURN: 
				//--user clicked the return key, quit program:
				CleanUp();			//call my clean up function
				PostQuitMessage(0); //put WM_QUIT message in the message queue
			break;
		} //end switch
		return 0;
	} // end msg switch
	return DefWindowProc(hwnd, iMsg, wParam, lParam); //let windows handle any messages if I haven't
}//end WindProc callback function
