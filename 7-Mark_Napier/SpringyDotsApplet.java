//SpringyDotsApplet.java is the main code for this applet.
//It includes code to display the applet, handle user interaction,
//and animate the 3 Dots object.

//SpringyObject.java is support code that simulates
//the behavior of springs and masses.

//Bitmap255.java is a library that handles the drawing of trails on screen.


public class SpringyDotsApplet extends Applet {
	SpringyDotsPanel dotPanel;

	public void init() {
		setBackground(Color.darkGray);
		setLayout(null);
		dotPanel = new SpringyDotsPanel(size().width, size().height);
		add(dotPanel);
		dotPanel.init();
	}

	public void start() {
		dotPanel.start();
	}

	public void stop() {
		dotPanel.stop();
	}

	public boolean mouseDown(Event e, int x, int y){
    		return dotPanel.mouseDown(e,x,y);
	}

	public boolean mouseDrag(Event e, int x, int y){
    		return dotPanel.mouseDrag(e,x,y);
	}

	public boolean mouseUp(Event e, int x, int y){
    		return dotPanel.mouseUp(e,x,y);
	}

	public void update(Graphics g) {
		paint(g);
	}
}


/************** Panel animates Springy Object  **************/

class SpringyDotsPanel extends Panel implements Runnable
{
	// to animate the panel
	Thread t;
	// to draw trails
	Bitmap255 BMP;
	// to handle physics stuff
	SpringyDots dots;
	Vector springs;
	Vector masses;
	// misc.
	int width = 0;
	int height = 0;
 	int counter = 40000;


	public SpringyDotsPanel(int width, int height) {
		setBounds(0,0,width,height);
		this.width = width;
		this.height = height;
	}


	public void init() {
		BMP = new Bitmap255(width,height);
		BMP.init();
		add(BMP);
		dots = new SpringyDots();
		springs = dots.springs;
		masses = dots.masses;
	}


	public boolean mouseDown(Event e, int x, int y) {
		return dots.grab(x,y);
	}


	public boolean mouseDrag(Event e, int x, int y) {
		return dots.drag(x,y);
	}


	public boolean mouseUp(Event e, int x, int y) {
		return dots.release(x,y);
	}


	public void paint(Graphics g) {
		Spring s = null;
		Mass m = null;
		int r = 0;

		// Move the dots a step
		dots.move();

		// Draw trails into image
		for (int i=0; i<springs.size(); i++){
			s = (Spring)springs.elementAt(i);
			if (s.visible) {
				BMP.drawLine(
					(int)s.mass1.x,
					(int)s.mass1.y,
					(int)s.mass2.x,
					(int)s.mass2.y  );
			}
		}

		// Draw image to screen
		BMP.paint(g);

		// Switch drawing from dark to lite periodically
		if (counter-- <= 0) {
			if (BMP.targetColorValue == 0.0F)
				BMP.targetColorValue = 255.0F;
			else
				BMP.targetColorValue = 0.0F;
			counter = 40000;
		}

		// draw springs to screen
		g.setColor(Color.green);
		for (int i=0; i<springs.size(); i++) {
			s = (Spring)springs.elementAt(i);
			if (s.visible) {
				g.drawLine(
					(int)s.mass1.x,
					(int)s.mass1.y,
					(int)s.mass2.x,
					(int)s.mass2.y  );
			}
		}

		// draw masses: larger mass makes bigger circle
		g.setColor(Color.cyan);
		for (int i=0; i<masses.size(); i++) {
			m = (Mass)masses.elementAt(i);
			r = m.m;
			g.drawOval((int)(m.x - r), (int)(m.y - r) ,r*2, r*2);
		}
	}


	public void update( Graphics g ) {
		paint(g);
	}


	public void start()	{
		if (t == null) {
			t = new Thread(this);
			t.start();
		}
	}


	public void stop() {
		t = null;
	}


	public void run() {
		while (t != null) {
			repaint();
			try {
				Thread.sleep(20);
			}
			catch(Exception e) {
				System.out.println(e);
			}
		}
	}
}


/************** Springy Dots Object **************/

class SpringyDots extends SpringyObject {
	public SpringyDots() {
		// Three masses connected by springs
		Spring s;
		Mass m0 = new Mass(300, 270);	// center point (fixed)
		Mass m1 = new Mass(170, 320);	// left
		Mass m2 = new Mass(300, 320);	// middle
		Mass m3 = new Mass(360, 320);	// right
		add(m0);
		add(m1);
		add(m2);
		add(m3);
		m0.setMovable(false);
		m0.setMass(2);
		m1.setMass(2);
		m2.setMass(5);
		m3.setMass(3);
		s = new Spring(m0, m2);
		s.setVisible(false);
		s.springConstant = 500;		// very mushy
		add(s);
		s = new Spring(m1, m2);
		s.springConstant = 1000;	// medium
		add(s);
		s = new Spring(m2, m3);
		s.springConstant = 3000;	// stiffer
		add(s);
	}
}





//SpringyObject.java

import java.util.*;


/************** Base class for objects made of springs **************/

class SpringyObject {
	Vector masses;
	Vector springs;
	Mass dragMass = null;
	Spring s = null;
	Mass m = null;
	float prevX = 0F;
	float prevY = 0F;

	public SpringyObject() {
		springs = new Vector();
		masses = new Vector();
	}

	public void add(Mass m) {
		masses.addElement(m);
	}

	public void add(Spring s) {
		springs.addElement(s);
	}

	public boolean grab(int x, int y) {
		Mass m = null;
		for (int i=0; i<masses.size(); i++){
			m = (Mass)masses.elementAt(i);
			if (m.distanceTo(x,y) < 35) {
				m.pressed = true;
				dragMass = m;
				break;
			}
		}
		if (dragMass != null) {
			prevX = dragMass.x;
			prevY = dragMass.y;
		}
		return true;
	}

	public boolean drag(int x, int y) {
		if (dragMass != null){
			prevX = dragMass.x;
			prevY = dragMass.y;
			dragMass.x = x;
			dragMass.y = y;
		}
		return true;
	}

	public boolean release(int x, int y) {
		if (dragMass != null){
			dragMass.pressed = false;
			dragMass.vX = 20*(x-prevX);
			dragMass.vY = 20*(y-prevY);
			dragMass = null;
		}
		return true;
	}

	public void move() {
		// Calc spring forces
		for (int i=0; i<springs.size(); i++){
			((Spring)springs.elementAt(i)).calculateForce();
		}

		// Calc new Mass positions
		for (int i=0; i<masses.size(); i++){
			((Mass)masses.elementAt(i)).calculateNewPositions();
		}
	}
}


/************** Spring **************/

class Spring {
	float springConstant = Global.springConstant;
	boolean visible = true;
	Mass mass1;
	Mass mass2;
	// used for calculations
	private float springLen = 0F;
	private float springMinLen = 0F;
	private float springMaxLen = 0F;
	private double tension = 0.0;
	private double lenX;
	private double lenY;
	private double lenNow;
	private double newlenX;
	private double newlenY;
	private double newlenNow;
	private double f;
	private double fX;
	private double fY;

	Spring(Mass m1, Mass m2){
		float lenX = m1.x - m2.x;
		float lenY = m1.y - m2.y;
		springLen = (float)Math.sqrt(((lenX*lenX) + (lenY*lenY)));
		springMinLen = (float)(springLen*Global.springMin);
		springMaxLen = (float)(springLen*Global.springMax);
		mass1 = m1;
		mass2 = m2;
	}

	void calculateForce(){
		lenX = mass2.x - mass1.x;
		lenY = mass2.y - mass1.y;
		lenNow = Math.sqrt(lenX * lenX + lenY * lenY);
		newlenX = lenX + ((mass2.vX - mass1.vX) / Global.vConstant);
		newlenY = lenY + ((mass2.vY - mass1.vY) / Global.vConstant);
		newlenNow = Math.sqrt(newlenX * newlenX + newlenY * newlenY);
		f = (Global.damping * Global.vConstant * (newlenNow - lenNow)) / lenNow;
		fX = (lenX * f) / lenNow;
		fY = (lenY * f) / lenNow;
		// change velocity of masses
		mass1.applyForce(fX, fY);
		mass2.applyForce(-fX, -fY);
		// cap the length
		if (lenNow < springLen / 2.0)
			lenNow = springLen / 2.0;
		else if (lenNow > springLen * 3.0 / 2.0)
			lenNow = springLen * 3.0 / 2.0;
		// calc tension of spring based on length
		tension = (springConstant * (springLen - lenNow)) / springLen;
		// calc force in x and y directions
		fX = (lenX * tension) / lenNow;
		fY = (lenY * tension) / lenNow;
		// apply the force to the masses
		mass1.applyForce(-fX, -fY);
		mass2.applyForce(fX, fY);
	}


	public void setVisible(boolean v) {
		visible = v;
	}
}


/************** Mass **************/

class Mass {
	int m = Global.mass;
	float x;
	float y;
	float vX;
	float vY;
	boolean pressed = false;
	boolean movable = true;
	boolean visible = true;

	Mass(int x, int y){
		this.x = x;
		this.y = y;
	}

	public void applyForce(double forceX, double forceY) {
		vX += Global.timeInterval * forceX / m;
		vY += Global.timeInterval * forceY / m;
	}

	void calculateNewPositions() {
		if (!movable || pressed)
			vX = vY = 0.0F;
		else {
			x += vX * Global.timeInterval;
			y += vY * Global.timeInterval;
		}
	}

	public void setMovable(boolean b)
	{
		movable = b;
	}

	public void setMass(int m)
	{
		this.m = m;
	}

	public double distanceTo(int px, int py) {
		return Math.sqrt((x-px)*(x-px) + (y-py)*(y-py));
	}
}


/************** Global Values **************/

class Global {
	static float springConstant = 1000;
	static float damping = 0.5F;
	static int   mass = 1;
	static float springMin = .5F;
	static float springMax = 2F;
	static float vConstant = 1000000.0F;
	static float timeInterval = 0.01F;
}
