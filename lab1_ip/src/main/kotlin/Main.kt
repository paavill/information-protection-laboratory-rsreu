import kotlin.random.Random

fun main(args: Array<String>) {
    val m = 2
    val k = 2
    val original = "Hi, how are you?"
    val grid = generateGrid(m, k)
    val encoded = encode(original, grid, m, k)
    val decoded = decode(encoded, grid, m, k)
    println("Encoded: " + encoded.flatten().joinToString(""))
    println("Decoded: " + decoded.joinToString(""))
}

fun generateGrid(m: Int, k: Int): List<List<Boolean>> {
    val result = MutableList(2 * k) { MutableList(2 * m) { true } }
    var size = m * k
    val maxI = 2 * k - 1
    val maxJ = 2 * m - 1
    val random = Random(System.currentTimeMillis())
    while (size > 0) {
        val i = random.nextInt(maxI)
        val j = random.nextInt(maxJ)
        val j180 = maxJ - j
        val i360 = maxI - i
        val j540 = maxJ - j180
        if (result[i][j] and result[i][j180] and result[i360][j180] and result[i360][j540]) {
            result[i][j] = false
            size -= 1
        }
    }
    return result
}

fun encode(original: String, grid: List<List<Boolean>>, m: Int, k: Int): List<List<String>> {
    val result = MutableList(2 * k) { MutableList(2 * m) { " " } }
    val originalList = original.toList().map { it.toString() }
    var counter = 0
    var ind = 0
    val maxI = 2 * k - 1
    val maxJ = 2 * m - 1
    result.forEachIndexed { i, strings ->
        strings.forEachIndexed { j, s ->
            if (!grid[i][j] && counter <= originalList.size && ind <= m * k) {
                val j180 = maxJ - j
                val i360 = maxI - i
                val j540 = maxJ - j180
                if (ind < originalList.size) {
                    result[i][j] = originalList[ind]
                    counter += 1
                    if (ind + m * k < originalList.size) {
                        result[i][j180] = originalList[ind + m * k]
                        counter += 1
                        if (ind + 2 * m * k < originalList.size) {
                            result[i360][j180] = originalList[ind + 2 * m * k]
                            counter += 1
                            if (ind + 3 * m * k < originalList.size) {
                                result[i360][j540] = originalList[ind + 3 * m * k]
                                counter += 1
                            }
                        }
                    }
                }
                ind += 1
            }
        }
    }
    return result
}

fun decode(original: List<List<String>>, grid: List<List<Boolean>>, m: Int, k: Int): List<String> {
    val result = mutableMapOf<Int, String>()
    var ind = 0
    val maxI = 2 * k - 1
    val maxJ = 2 * m - 1
    grid.forEachIndexed { i, row ->
        row.forEachIndexed { j, s ->
            if (!grid[i][j] && ind <= m * k) {
                val j180 = maxJ - j
                val i360 = maxI - i
                val j540 = maxJ - j180
                result[ind] = original[i][j]
                result[ind + m * k] = original[i][j180]
                result[ind + 2 * m * k] = original[i360][j180]
                result[ind + 3 * m * k] = original[i360][j540]
                ind += 1
            }
        }
    }
    val sortedResult = result.toSortedMap()
    return sortedResult.values.toList()
}