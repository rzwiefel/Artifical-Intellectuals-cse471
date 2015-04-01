package cse471_part1_genetic;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Random;


public class Genetic {
	public static final String FILENAME = "348.edges.txt";
	public static HashMap<Integer, Integer> loc = null;
	public static int count;

	public static void main(String[] args) {
		ArrayList<Integer[]> inputList = new ArrayList<>();
		try {
			BufferedReader br = new BufferedReader(new FileReader(FILENAME));
			String line = "";
			while ((line = br.readLine()) != null) {
				String[] numstr = line.split(" ");
				inputList.add(new Integer[] {Integer.parseInt(numstr[0]), Integer.parseInt(numstr[1])});
			}
			br.close();
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
		ArrayList<Integer> unexposed = new ArrayList<>();
		count = (int) inputList.stream().mapToInt(arr -> {return arr[0];}).distinct().count();
		loc = new HashMap<>();
		int im = 0;
		for(Integer i : inputList.stream().mapToInt(a -> a[0]).distinct().toArray()) {
			loc.put(i, im++);
			unexposed.add(i);
		}

		boolean[][] graph = new boolean[count][count];
		for (Integer[] arr : inputList) {
			makeFriend(graph, loc.get(arr[0]), loc.get(arr[1]));
		}

	}

	public static void makeFriend(boolean[][] graph, Integer i, Integer j) {
		graph[i][j] = true;
		graph[j][i] = true;
	}

	public static boolean[][] copyGraph(boolean[][] graph) {
		boolean[][] newGraph = new boolean[count][count];
		for (int i = 0; i < count; ++i) {
			for (int j = 0; j < count; ++j) {
				newGraph[i][j] = graph[i][j];
			}
		}
		return newGraph;
	}

	public static List<Integer> copyList(List<Integer> toCopy) {
		List<Integer> copied = new ArrayList<>();
		for (Integer i : toCopy) {
			int _i = i;
			copied.add(_i);
		}
		return copied;
	}

	public static float fitness(boolean[][] _graph, List<Integer> _unexposed, List<Integer> node) {
		float fitness = 0;
		boolean[][] graph = copyGraph(_graph);
		List<Integer> unexposed = copyList(_unexposed);
		for (int i = 0; i < node.size(); ++i) {
			if (!unexposed.contains(node.get(i))) {
				continue;
			}
			int n_exposed = count - unexposed.size();
			int n_given_card = i;
			List<Integer> new_exposed_people = neighbors(graph, node.get(i));
			int new_exposed = new_exposed_people.size();
			float adoption_prob = 0f;
			if (n_exposed + n_given_card != 0) adoption_prob = (float) Math.max(.1, 1-1/(n_exposed + n_given_card));
			else adoption_prob = .1f;
			fitness += 1 + new_exposed * adoption_prob;

			unexposed.removeAll(new_exposed_people);
			unexposed.remove(Integer.valueOf(node.get(i)));
		}
		return fitness;
	}

	public static List<Integer> neighbors(boolean[][] graph, int person) {
		List<Integer> neighbors = new ArrayList<>();
		for (int i = 0; i < count; ++i) {
			if (graph[person][i]) neighbors.add(i);
		}
		return neighbors;
	}

	public static void crossover(List<Integer> n1, List<Integer> n2) {
		int crossover_point = new Random().nextInt(n1.size()-1) + 1;
		for (int i = 0; i < n1.size(); ++i) {
			int temp;
			if (i < crossover_point) continue;
			temp = n1.get(i);
			n1.set(i, n2.get(i));
			n2.set(i, temp);
		}
	}

	public static void mutate(List<Integer> population, List<Integer> node) {
		int rand_index = new Random().nextInt(node.size());
		int rand_person = new Random().nextInt(population.size());
		if (node.stream().anyMatch(i -> population.get(rand_person) == i)) {
			mutate(population, node);
		} else {
			node.set(rand_index, population.get(rand_person));
		}

	}
}
