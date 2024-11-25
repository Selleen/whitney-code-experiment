import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.layout.StackPane;
import javafx.scene.paint.Color;
import javafx.stage.Stage;

public class CountryHighlighterApp extends Application {

    @Override
    public void start(Stage primaryStage) {
        Canvas canvas = new Canvas(800, 600);
        GraphicsContext gc = canvas.getGraphicsContext2D();

        // Dibuja un rectángulo como ejemplo
        gc.setFill(Color.LIGHTGRAY);
        gc.fillRect(0, 0, canvas.getWidth(), 50);

        // Agrega lógica para mostrar texto y resaltar país
        gc.setFill(Color.BLACK);
        gc.fillText("Nombre del país", 100, 30);

        // Crea la escena y muestra la ventana
        StackPane root = new StackPane(canvas);
        Scene scene = new Scene(root, 800, 600);
        primaryStage.setTitle("Country Highlighter");
        primaryStage.setScene(scene);
        primaryStage.show();
    }

    public static void main(String[] args) {
        launch(args);
    }
}
