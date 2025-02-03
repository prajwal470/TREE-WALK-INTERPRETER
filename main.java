import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
	public static void main(String[] args) throws IOException {
		runPrompt();
	}

	private static void runPrompt() throws IOException {
		InputStreamReader input = new InputStreamReader(System.in);
		BufferedReader reader = new BufferedReader(input);
		for (;;) {
			System.out.print("> ");
			String line = reader.readLine();
			if (line == null) break;
			run(line);
		}
	}

	private static void run(String line) {
		// Implementation of run method
		System.out.println("Running: " + line);
	}
}