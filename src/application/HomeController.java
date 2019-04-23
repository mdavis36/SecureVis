package application;

import java.io.File;
import java.io.IOException;
import java.net.URL;
import java.util.ResourceBundle;

import javafx.application.Platform;
import javafx.beans.InvalidationListener;
import javafx.beans.Observable;
import javafx.beans.binding.Bindings;
import javafx.beans.property.DoubleProperty;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.Button;
import javafx.scene.control.ComboBox;
import javafx.scene.control.Slider;
import javafx.scene.layout.VBox;
import javafx.scene.media.Media;
import javafx.scene.media.MediaPlayer;
import javafx.scene.media.MediaView;
import javafx.scene.text.Text;
import javafx.util.Duration;
import main.Communication;
import main.StreamingPageRow;

public class HomeController implements Initializable {
	
	@FXML private Button playButton;
	@FXML private Button pauseButton;
	@FXML private Button restartButton;
	@FXML private MediaView videoView;
	@FXML private Slider videoSlider;
	@FXML private VBox streamingPage;
	@FXML private ComboBox<String> rooms;
	@FXML private ComboBox<String> dates;
	private MediaPlayer videoPlayer;
	private Media video;
	
	private static final String GET_ROOMS = "Rooms";
	private static final String GUI = "GUI";
	
	@Override
	public void initialize(URL location, ResourceBundle resources) {
		// set file path for testing
		String videoPath = new File("testFootage/test480.mp4").getAbsolutePath();
		
		// setup test footage in MediaView
		video = new Media(new File(videoPath).toURI().toString());
		videoPlayer = new MediaPlayer(video);
		videoView.setMediaPlayer(videoPlayer);
		// videoPlayer.setAutoPlay(false);
		
		// scale video in window
		DoubleProperty videoWidth = videoView.fitWidthProperty();
		DoubleProperty videoHeight = videoView.fitHeightProperty();
		videoWidth.bind(Bindings.selectDouble(videoView.sceneProperty(), "width"));
		videoHeight.bind(Bindings.selectDouble(videoView.sceneProperty(), "height"));
		
		// video slider functionality 
	    videoPlayer.currentTimeProperty().addListener(new InvalidationListener() {
	    	
	    	@Override
			public void invalidated(Observable o) {
	    		updateSliderValue();
			} 
	    }); 

	    // slider jumping event listener
	    videoSlider.valueProperty().addListener(new InvalidationListener() {
	    	
	    	@Override
	        public void invalidated(Observable o) 
	        { 
	            if (videoSlider.isPressed()) {
	            	Duration vidDuration = videoPlayer.getMedia().getDuration();
	            	
	            	// set current video time with slider
	                videoPlayer.seek(vidDuration.multiply(videoSlider.getValue() / 100.0)); 
	            } 
	        } 
	    });  
	}
	
	@FXML // play current video
	public void playVideo() {
		videoPlayer.play();
	}
	
	@FXML // pause current video
	public void pauseVideo() {
		videoPlayer.pause();
	}
	
	@FXML // restart current video
	public void restartVideo() {
		videoPlayer.seek(videoPlayer.getStartTime());
		// videoPlayer.stop();
	}    
	 
    public void updateSliderValue() 
    { 
        Platform.runLater(new Runnable() { 
            public void run() 
            { 
            	double vidCurrentMillis = videoPlayer.getCurrentTime().toMillis();
            	double vidDurationMillis = videoPlayer.getTotalDuration().toMillis();
            	
                // moves slider while video plays
                videoSlider.setValue(vidCurrentMillis / vidDurationMillis * 100.0);
            } 
        }); 
    } 
    
    @FXML // display rooms for streaming
    public void displayRooms() {
    	Communication connect;
    	streamingPage.getChildren().clear();
    	try {
			connect = new Communication(GUI + GET_ROOMS);
			String numberRoomsString = connect.getReturnMessage();			
			int numRooms = Integer.getInteger(numberRoomsString);			
			generateRooms(numRooms);
		} catch (ClassNotFoundException | IOException e) {
			Text error = new Text("Cannot connect to master system");
			//generateRooms(4);
			streamingPage.getChildren().add(error);
		}
    }
    
    private void generateRooms(int numRooms) {
		for (int i = 0; i < numRooms; i++) {
			streamingPage.getChildren().add(new StreamingPageRow("TEST", 5));
		}		
	}
    
    @FXML // display rooms for streaming
    public void displayRoomsForVideo() {
    	Communication connect;
    	// rooms.
    	try {
			connect = new Communication(GUI + GET_ROOMS);			
			String numberRoomsString = connect.getReturnMessage();			
			int numRooms = Integer.getInteger(numberRoomsString);			
			generateRooms(numRooms);
		} catch (ClassNotFoundException | IOException e) {
			Text error = new Text("Cannot connect to master system");
			//generateRooms(4);
			streamingPage.getChildren().add(error);
		}
    }
}
