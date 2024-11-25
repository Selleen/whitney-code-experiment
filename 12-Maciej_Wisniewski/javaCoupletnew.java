import javax.swing.*;
import java.awt.*;

public class Couplet extends JFrame {
    private int grayScale; // Almacena el valor del fondo
    private String line1, line2, line3; // Textos a mostrar

    // Constructor para inicializar parámetros
    public Couplet(int grayScale, String line1, String line2, String line3) {
        this.grayScale = Math.min(255, Math.max(0, grayScale)); // Restringir entre 0-255
        this.line1 = line1;
        this.line2 = line2;
        this.line3 = line3;
        initializeUI();
    }

    // Configura la ventana
    private void initializeUI() {
        setTitle("The Meaning of Life as Expressed in Seven Lines of Code");
        setSize(400, 200);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null);
    }

    @Override
    public void paint(Graphics g) {
        super.paint(g);
        // Establece el color de fondo
        getContentPane().setBackground(new Color(grayScale, grayScale, grayScale));

        // Dibuja las líneas de texto
        g.setColor(Color.BLACK);
        g.drawString(line1, 50, 70);
        g.drawString(line2, 50, 100);
        g.drawString(line3, 50, 130);
    }

    public static void main(String[] args) {
        // Ejemplo de parámetros
        int grayScale = 128; // Color gris medio
        String line1 = "The meaning of life is.. 42";
        String line2 = "The meaning of life is... Keep going";
        String line3 = "The meaning of life is.... Enjoy the journey";

        // Crear y mostrar la ventana
        SwingUtilities.invokeLater(() -> {
            Couplet couplet = new Couplet(grayScale, line1, line2, line3);
            couplet.setVisible(true);
        });
    }
}
