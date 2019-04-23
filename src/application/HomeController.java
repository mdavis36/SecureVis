package application;

import javafx.fxml.FXML;
import javafx.scene.control.Button;
import javafx.scene.media.Media;
import javafx.scene.media.MediaPlayer;
import javafx.scene.media.MediaView;

public class HomeController {
	
	@FXML private Button playButton;
	@FXML private Button pauseButton;
	@FXML private Button restartButton;
	@FXML private MediaView videoView;
	private MediaPlayer videoPlayer;
	private Media video;
	
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
	}
}
