package application;

import java.io.File;
import java.time.LocalDate;
import java.util.ArrayList;

import javafx.scene.text.Text;

public class DirectoryUtil {

	public static final String VIDEO_DIRECTORY = "testFootage";
	
	
	// Returns files in video directory based on date and name
	public static ArrayList<String> filesByDateAndName(String date,String rName) {
		
		File directory = new File(VIDEO_DIRECTORY);
		File[] filesInDir = directory.listFiles();
		ArrayList<String> files = new ArrayList<String>();
		
		for (int i = 0; i < filesInDir.length; i++) {
			if (filesInDir[i].getName().contains(date) && filesInDir[i].getName().contains(rName)) {
				files.add(filesInDir[i].getName());
			}
		}
		
		return files;
	}
	
	// creates date string based on how SecureVis stores dates
	public static String parseDate(LocalDate date) {
		String rtDate = "" + date.getYear(); 
		if(date.getMonthValue() < 10) {
			rtDate += "0" + date.getMonthValue();
		} else {
			rtDate += date.getMonthValue();
		}
		
		if (date.getDayOfMonth() < 10) {
		 rtDate	+= "0" + date.getDayOfMonth();
	
		} else {
			rtDate += date.getDayOfMonth();
		}
		 
		 return rtDate;
	
	}
	
	// returns a list of rooms given a date
	public static ArrayList<String> findRoomsByDate(String dateFormat) {
		File directory = new File(VIDEO_DIRECTORY);
		File[] filesInDir = directory.listFiles();
		ArrayList<String> rooms = new ArrayList<String>();
		for (int i = 0; i < filesInDir.length; i++) {
			if (filesInDir[i].getName().contains(dateFormat)) {
				String roomName = filesInDir[i].getName().split("_")[0];
				if (!(rooms.contains(roomName))) {
					rooms.add(roomName);
				}
			}
		}
		return rooms;
	}
	
	public static ArrayList<String> allDates() {
		File directory = new File(VIDEO_DIRECTORY);
		File[] filesInDir = directory.listFiles();
		ArrayList<String> dates = new ArrayList<String>();
		
		for (File file : filesInDir) {
			String[] split = file.getName().split("_");
			if (split.length == 4) {
				String date = split[1];
				if (!dates.contains(date)) {
					dates.add(date);
				}
			}
		}
		return dates;
	}
}
