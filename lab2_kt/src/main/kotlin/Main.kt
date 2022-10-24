import kotlin.math.roundToInt
import kotlin.math.sqrt
import kotlin.random.Random

fun main(args: Array<String>) {
    val original = "Codetest"
    val password = "1234"
    val codePage =
        " !\"#\$%&\\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"
    val grid = generateGrid(false, codePage)
    val encoded = encode(original, grid)
    val encodedPassword = encode(password, grid)
    val encodedString = encoded.joinToString("") + encodedPassword.joinToString("")
    println("Encoded: $encodedString")
    val pass = encodedString.slice((encodedString.length - password.length) until encodedString.length)
    val decodedPass = decode(pass.toList().map { it.toString() }, grid)
    if (decodedPass.joinToString("") == password) {
        val decoded = decode(encoded.slice(0 until (encodedString.length - password.length)), grid)
        println("Decoded: " + decoded.joinToString(""))
    } else {
        println("Wrong password!")
    }
}

fun generateGrid(shuffle: Boolean, codePage: String): List<List<String>> {
    val result = codePage.toList().map { it.toString() }.toMutableList()
    val width = sqrt(result.size.toDouble()).roundToInt()
    while (result.size % width != 0) {
        result.add(" ")
    }
    return generateGrid(width, result, shuffle)
}

fun generateGrid(width: Int, charactersList: List<String>, shuffle: Boolean): List<List<String>> {
    val shuffledList = if (shuffle) {
        charactersList.shuffled()
    } else {
        charactersList
    }
    return shuffledList.chunked(width)
}

fun findXY(element: String, grid: List<List<String>>): Pair<Int, Int> {
    grid.forEachIndexed { i, row ->
        row.forEachIndexed { j, e ->
            if (grid[i][j] == element) {
                return Pair(i, j)
            }
        }
    }
    throw Exception("Element not found!")
}

fun encode(original: String, grid: List<List<String>>): List<String> {
    val result = mutableListOf<String>()
    val originalChunked = original.toList().map { it.toString() }.chunked(2)
    originalChunked.forEach {
        if (it.size == 2 && it[0] != it[1]) {
            val xy0 = findXY(it[0], grid)
            val xy1 = findXY(it[1], grid)
            result.add(grid[xy0.first][xy1.second])
            result.add(grid[xy1.first][xy0.second])
        } else {
            result.add(it[0])
            result.add("sys")
        }
    }
    return result
}

fun decode(original: List<String>, grid: List<List<String>>): List<String> {
    val result = mutableListOf<String>()
    val originalChunked = original.chunked(2)
    originalChunked.forEach {
        if (it.size == 2 && it[1] != "sys") {
            val xy0 = findXY(it[0], grid)
            val xy1 = findXY(it[1], grid)
            result.add(grid[xy0.first][xy1.second])
            result.add(grid[xy1.first][xy0.second])
        } else {
            result.add(it[0])
            result.add(it[0])
        }
    }
    return result
}