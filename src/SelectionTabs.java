import javafx.scene.control.Button;
import javafx.scene.layout.HBox;

public class SelectionTabs extends HBox {
	
	SelectionTabs() {
		super();
		
		Button videoPageButton = new Button("VIDEO");
		Button settingsPageButton = new Button("SETTINGS");
		
		this.getChildren().addAll(videoPageButton,settingsPageButton);
		
	}
}
