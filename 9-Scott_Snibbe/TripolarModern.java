import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

// Tripolar by Scott Snibbe. Modernized for Java 8+
// Simulates a pendulum swinging above three magnets with chaotic behavior.

public class TripolarModern extends JPanel implements Runnable, MouseListener, MouseMotionListener {
    private Thread animationThread;
    private boolean running;
    private int speed = 33;
    private Image offScreenImage;
    private Graphics offScreenGraphics;
    private int screenWidth, screenHeight;
    private double centerX, centerY, scale;
    private Point mousePt = new Point();
    private boolean mousePressed = false;
    private double probeX = Double.MAX_VALUE, probeY = Double.MAX_VALUE;

    // Simulation parameters
    private final double damping = 0.97;
    private final double gravity = 0.005;
    private final double magnetism = 0.1;
    private final double height = 0.1;
    private final double mass = 1.0;
    private final double timeStep = 0.01;
    private final double[] magnetX = new double[3];
    private final double[] magnetY = new double[3];

    public TripolarModern() {
        setBackground(Color.WHITE);
        addMouseListener(this);
        addMouseMotionListener(this);
    }

    @Override
    public void run() {
        while (running) {
            updateAnimation();
            repaint();
            try {
                Thread.sleep(speed);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
    }

    public void start() {
        running = true;
        animationThread = new Thread(this);
        animationThread.start();
    }

    public void stop() {
        running = false;
    }

    @Override
    public void paintComponent(Graphics g) {
        super.paintComponent(g);
        if (offScreenImage == null) {
            screenWidth = getWidth();
            screenHeight = getHeight();
            centerX = screenWidth / 2.0;
            centerY = screenHeight / 2.0;
            scale = Math.min(centerX, centerY);
            offScreenImage = createImage(screenWidth, screenHeight);
            offScreenGraphics = offScreenImage.getGraphics();
            setMagnets(0.5);
        }

        offScreenGraphics.setColor(Color.WHITE);
        offScreenGraphics.fillRect(0, 0, screenWidth, screenHeight);

        if (probeX != Double.MAX_VALUE) {
            updatePaths((probeX - centerX) / scale, (probeY - centerY) / scale, offScreenGraphics);
        }

        g.drawImage(offScreenImage, 0, 0, this);
    }

    private void setMagnets(double radius) {
        for (int i = 0; i < 3; i++) {
            double angle = Math.PI / 2 + (2 * Math.PI / 3) * i;
            magnetX[i] = radius * Math.cos(angle);
            magnetY[i] = radius * Math.sin(angle);
        }
    }

    private void updateAnimation() {
        if (!mousePressed) return;

        if (probeX == Double.MAX_VALUE) {
            probeX = mousePt.x;
            probeY = mousePt.y;
        }

        double dx = mousePt.x - probeX;
        double dy = mousePt.y - probeY;

        if (dx * dx + dy * dy > 1) {
            probeX += dx / 2;
            probeY += dy / 2;
        } else {
            probeX += dx * 0.01;
            probeY += dy * 0.01;
        }
    }

    private void updatePaths(double x, double y, Graphics g) {
        double vX = 0, vY = 0;
        double filtVel = 1;
        int iterations = 0;
        g.setColor(Color.BLACK);

        while (filtVel > 0.1 && iterations < 10000) {
            iterations++;
            double fX = 0, fY = 0;
            double r = x * x + y * y;

            if (r < 0.00001) r = 0.00001;
            fX -= (x * gravity) / r;
            fY -= (y * gravity) / r;

            for (int m = 0; m < 3; m++) {
                double dx = magnetX[m] - x;
                double dy = magnetY[m] - y;
                double dist = Math.sqrt(dx * dx + dy * dy + height * height);
                if (dist < 0.00001) dist = 0.00001;
                double force = magnetism / (dist * dist * dist);
                fX += force * dx;
                fY += force * dy;
            }

            fX -= vX * damping;
            fY -= vY * damping;

            vX += timeStep * fX / mass;
            vY += timeStep * fY / mass;

            filtVel = 0.99 * filtVel + 0.1 * Math.max(Math.abs(vX), Math.abs(vY));

            double nextX = x + vX;
            double nextY = y + vY;
            drawLine(x, y, nextX, nextY, g);
            x = nextX;
            y = nextY;
        }
    }

    private void drawLine(double x1, double y1, double x2, double y2, Graphics g) {
        g.drawLine((int) (x1 * scale + centerX), (int) (y1 * scale + centerY),
                   (int) (x2 * scale + centerX), (int) (y2 * scale + centerY));
    }

    @Override
    public void mousePressed(MouseEvent e) {
        mousePressed = true;
        mousePt.setLocation(e.getPoint());
    }

    @Override
    public void mouseReleased(MouseEvent e) {
        mousePressed = false;
    }

    @Override
    public void mouseDragged(MouseEvent e) {
        if (mousePressed) {
            mousePt.setLocation(e.getPoint());
        }
    }

    @Override public void mouseMoved(MouseEvent e) {}
    @Override public void mouseClicked(MouseEvent e) {}
    @Override public void mouseEntered(MouseEvent e) {}
    @Override public void mouseExited(MouseEvent e) {}

    public static void main(String[] args) {
        JFrame frame = new JFrame("Tripolar Simulation");
        TripolarModern simulation = new TripolarModern();
        frame.add(simulation);
        frame.setSize(800, 800);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setVisible(true);
        simulation.start();
    }
}
