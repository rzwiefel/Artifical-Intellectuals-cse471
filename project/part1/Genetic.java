
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.PrintWriter;
import java.io.FileWriter;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Random;
import java.util.stream.Collectors;
import java.util.stream.IntStream;


public class Main {
	public static final String FILENAME = "348.edges.txt";
	public static HashMap<Integer, Integer> loc = null;
	public static int count;
	public static volatile double globalMaxFitness = 0d;
	public static volatile List<Integer> globalMaxFitnessNode = null;
	public static Object fileLock = new Object();
	public static final String OUTFILENAME = "genetic_algorithm_output.txt";

	public static void main(String[] args) {
		long start = System.nanoTime();
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
		HashMap<Integer, Integer> revloc = new HashMap<>();
		int im = 0;
		for(Integer i : inputList.stream().mapToInt(a -> a[0]).distinct().toArray()) {
			loc.put(i, im);
			revloc.put(im, i);
			unexposed.add(im++);
		}
//		List<Integer> tl = new ArrayList<>();// {208, 203, 77, 57, 75, 26, 160, 114, 53, 9} ;
//		tl.add(208);tl.add(203);tl.add(77);tl.add(57);tl.add(75);tl.add(26);tl.add(160);tl.add(114);tl.add(53);tl.add(9);
//		tl.forEach(p -> System.out.print(" " + revloc.get(p)));
//		System.exit(0);

		boolean[][] graph = new boolean[count][count];
		for (Integer[] arr : inputList) {
			makeFriend(graph, loc.get(arr[0]), loc.get(arr[1]));
		}

		int n = 10; //Number of cards
		int k = 100; //Number of nodes per thread
		int iterations = 1000000;
		double mutationProb = 0.05;

		List<Thread> threadList = new ArrayList<>();
		int tcount = 12;//Runtime.getRuntime().availableProcessors();
		for (int i = 0; i < tcount; ++i) {
			Thread t = new Thread(() -> geneticAlgorithm(graph, unexposed, n, k, iterations, mutationProb));
			threadList.add(t);
		}
		threadList.forEach(Thread::start);

		threadList.forEach(t -> {try {t.join();}catch(Exception e){e.printStackTrace();};});
		System.out.println("All finished. (in " + (System.nanoTime()-start)/1000000000 + " s)");


	}//end of Main function

	public static void geneticAlgorithm(boolean[][] graph, List<Integer> unexposed, int n, int k, int iter, double mutProb) {
		double maxFitness = 0;
		List<Integer> maxFitnessNode = null;
		final List<List<Integer>> population = new ArrayList<>();
		IntStream.range(0, k).forEach(i -> population.add(randNode(graph, n)));

		for (int iterNum = 0; iterNum < iter; ++iterNum) {
			List<Double> fitnesses = population.stream()
					.mapToDouble(p -> fitness(graph, unexposed, p))
					.boxed()
					.collect(Collectors.toList());
			double curmax = fitnesses.stream().mapToDouble(Double::doubleValue).max().getAsDouble();
			if (maxFitness < curmax) {
				maxFitness = curmax;
				maxFitnessNode = population.get(fitnesses.indexOf(curmax));
				if (globalMaxFitness < maxFitness) {
					updateMax(maxFitness, maxFitnessNode);
				}
			}
			final List<Double> reproProb = reproductionProbibilityDistribution(fitnesses);
			IntStream.range(0, (int)Math.floor(population.size()))
					.forEach(i -> {
						int n1i = getReproductionCandidate(reproProb, -1);
						int n2i = getReproductionCandidate(reproProb, n1i);
						crossover(population.get(n1i), population.get(n2i));
						if (Math.random() < mutProb) {
							mutate(unexposed, population.get(n1i));
						}
						if (Math.random() < mutProb) {
							mutate(unexposed, population.get(n2i));
						}
					});
		}//end of outer For
	}

	public static void updateMax(double newMax, List<Integer> node) {
		synchronized (Main.class) {
			if (newMax < globalMaxFitness) return;
			globalMaxFitness = newMax;
			globalMaxFitnessNode = node;
			System.out.println("New Global Max: " + newMax + ".");
			node.forEach(i -> System.out.print(" " + i));
			System.out.println();
		}
		final double m = newMax;
		final List<Integer> n = node;
		Thread t = new Thread(() -> {
			synchronized (fileLock) {
				PrintWriter pw = null;
				try {
					pw = new PrintWriter(new BufferedWriter(new FileWriter(OUTFILENAME, true)));
					pw.write("New Global Max: " + m + ".");
					final StringBuilder sb = new StringBuilder();
					n.forEach(i -> sb.append(" " + i));
					pw.write(sb.toString() + "\r\n");
				} catch (Exception e) {
					e.printStackTrace();
				} finally {
					if (pw != null) {
						pw.flush();
						pw.close();
					}
				}
			}
		});
		//t.setDaemon(true);
		t.start();
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

	public static <T> List<T> copyList(List<T> toCopy) {
		List<T> copied = new ArrayList<>();
		for (T i : toCopy) {
			T _i = i;
			copied.add(_i);
		}
		return copied;
	}

	public static double fitness(boolean[][] _graph, List<Integer> _unexposed, List<Integer> node) {
		float fitness = 0;
		boolean[][] graph = _graph;//copyGraph(_graph);
		List<Integer> unexposed = copyList(_unexposed);
		for (int i = 0; i < node.size(); ++i) {
			if (!unexposed.contains(node.get(i))) {
				continue;
			}
			int n_exposed = count - unexposed.size();
			int n_given_card = i;
			List<Integer> new_exposed_people = neighbors(graph, node.get(i));
			int new_exposed = new_exposed_people.size();
			double adoption_prob = 0;
			if (n_exposed + n_given_card != 0) adoption_prob = (double) Math.max(.1, 1-1/(n_exposed + n_given_card));
			else adoption_prob = .1;
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

	public static List<Double> reproductionProbibilityDistribution(List<Double> fitnesses) {
		double fitnessSum = fitnesses.stream().reduce(0d, Double::sum);
		return fitnesses.stream().map(i -> i/fitnessSum).collect(Collectors.toList());
	}

	public static int getReproductionCandidate(List<Double> fpd, int excludeIdx) {
		double maxProb = 1d;
		List<Double> _fpd = fpd;
		if (excludeIdx > -1) {
			_fpd = copyList(fpd);
			maxProb -= _fpd.remove(excludeIdx);
		}
		double rand = Math.random() * maxProb;
		double probSum = 0d;
		for (int i = 0; i < _fpd.size(); ++i) {
			probSum += _fpd.get(i);
			if (rand < probSum) {
				return i;
			}
		}
		return 0; // Should never happen...
	}

	public static int randPerson(boolean[][] graph) {
		return new Random().nextInt(graph.length);
	}

	public static List<Integer> randNode(boolean[][] graph, int size) {
		//if(size>graph.length) {System.out.println("fuckoff");System.exit(-1);}
		List<Integer> node = new ArrayList<>();
		while (node.size() < size) {
			int randPerson = randPerson(graph);
			if (!node.contains(randPerson)) {
				node.add(randPerson);
			}
		}
		return node;
	}








}//end of class Main
