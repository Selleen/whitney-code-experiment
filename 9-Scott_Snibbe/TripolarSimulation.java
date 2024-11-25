import javax.swing.*;
import java.awt.*;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;

public class TripolarSimulation extends JPanel implements Runnable {
    private Thread animationThread = null;
    private boolean running = false;
    private int speed = 33;
    private int screenWidth, screenHeight;
    private double centerX, centerY, scale;
    private boolean mousePressed = false;
    private Point mousePoint = new Point();
    private double probeX = 1e10, probeY = 1e10;
    private double damping = 0.97;
    private double gravity = 0.005;
    private double magnetism = 0.1;
    private double height = 0.1;
    private double mass = 1.0;
    private double dtSim = 0.01;
    private double[] magnetX, magnetY;

    public TripolarSimulation() {
        setPreferredSize(new Dimension(800, 800));
        setBackground(Color.WHITE);
        magnetX = new double[3];
        magnetY = new double[3];
        setMagnets(0.5);

        addMouseListener(new MouseAdapter() {
            @Override
            public void mousePressed(MouseEvent e) {
                mousePressed = true;
                mousePoint = e.getPoint();
            }

            @Override
            public void mouseReleased(MouseEvent e) {
                mousePressed = false;
            }
        });

        addMouseMotionListener(new MouseAdapter() {
            @Override
            public void mouseDragged(MouseEvent e) {
                if (mousePressed) {
                    mousePoint = e.getPoint();
                }
            }
        });
    }

    public void start() {
        if (animationThread == null) {
            animationThread = new Thread(this);
            running = true;
            animationThread.start();
        }
    }

    public void stop() {
        running = false;
        if (animationThread != null) {
            try {
                animationThread.join();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            animationThread = null;
        }
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

    private void setMagnets(double r) {
        magnetX[0] = r * Math.cos(Math.PI / 2);
        magnetY[0] = r * Math.sin(Math.PI / 2);
        magnetX[1] = r * Math.cos(Math.PI / 2 + (2 * Math.PI) / 3);
        magnetY[1] = r * Math.sin(Math.PI / 2 + (2 * Math.PI) / 3);
        magnetX[2] = r * Math.cos(Math.PI / 2 - (2 * Math.PI) / 3);
        magnetY[2] = r * Math.sin(Math.PI / 2 - (2 * Math.PI) / 3);
    }

    private void updateAnimation() {
        if (!mousePressed) return;

        if (probeX == 1e10) {
            probeX = mousePoint.x;
            probeY = mousePoint.y;
        }

        double dx = mousePoint.x - probeX;
        double dy = mousePoint.y - probeY;
        double distSq = dx * dx + dy * dy;
        if (distSq > 1) {
            probeX += dx / 2;
            probeY += dy / 2;
        } else {
            probeX += dx * 0.01;
            probeY += dy * 0.01;
        }
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        Graphics2D g2d = (Graphics2D) g;
        g2d.setColor(Color.BLACK);

        screenWidth = getWidth();
        screenHeight = getHeight();
        centerX = screenWidth / 2.0;
        centerY = screenHeight / 2.0;
        scale = Math.min(centerX, centerY);

        if (probeX != 1e10) {
            updatePaths((probeX - centerX) / scale, (probeY - centerY) / scale, g2d);
        }
    }

    private void updatePaths(double x, double y, Graphics2D g) {
        double vX = 0, vY = 0;
        double filtVel = 1;
        int iter = 0;

        while (filtVel > 0.1 && iter < 10000) {
            iter++;
            double fX = 0, fY = 0;

            double r = x * x + y * y;
            r = Math.max(r, 0.00001);
            double over_rsq = 1.0 / r;
            fX -= (x * gravity) * over_rsq;
            fY -= (y * gravity) * over_rsq;

            for (int m = 0; m < 3; m++) {
                double dx = magnetX[m] - x;
                double dy = magnetY[m] - y;
                r = Math.sqrt(dx * dx + dy * dy + height * height);
                r = Math.max(r, 0.00001);
                double over_rcube = 1.0 / (r * r * r);
                fX += magnetism * dx * over_rcube;
                fY += magnetism * dy * over_rcube;
            }

            fX -= vX * damping;
            fY -= vY * damping;

            vX += dtSim * fX / mass;
            vY += dtSim * fY / mass;

            filtVel = 0.99 * filtVel + 0.1 * Math.max(Math.abs(vX), Math.abs(vY));

            double lastX = x;
            double lastY = y;
            x += vX;
            y += vY;

            drawNormalizedLine(lastX, lastY, x, y, g);
        }
    }

    private void drawNormalizedLine(double x1, double y1, double x2, double y2, Graphics2D g) {
        g.drawLine(
                (int) Math.round(x1 * scale + centerX),
                (int) Math.round(y1 * scale + centerY),
                (int) Math.round(x2 * scale + centerX),
                (int) Math.round(y2 * scale + centerY)
        );
    }

    public static void main(String[] args) {
        JFrame frame = new JFrame("Tripolar Simulation");
        TripolarSimulation simulation = new TripolarSimulation();

        frame.add(simulation);
        frame.pack();
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setVisible(true);

        simulation.start();
    }
}
