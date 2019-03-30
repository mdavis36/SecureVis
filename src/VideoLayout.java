import javafx.scene.layout.BorderPane;

public class VideoLayout extends BorderPane {
	VideoLayout(){
		super();
		this.setTop(new SelectionTabs());
	}
}
