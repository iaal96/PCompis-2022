program transpuestaMatriz;

main() {
    var int i, j, matrix[3][3], result[3][3];
        
    %% assign matrix
    matrix[0][0] = 1;
    matrix[1][0] = 4;
    matrix[2][0] = 7;
    matrix[0][1] = 2;
    matrix[1][1] = 5;
    matrix[2][1] = 8;
    matrix[0][2] = 3;
    matrix[1][2] = 6;
    matrix[2][2] = 9;

    result = matrix!;

    for j = 0 to j < 3 {
        for i = 0 to i < 3 {
            print(result[i][j]);
        }
    }
}