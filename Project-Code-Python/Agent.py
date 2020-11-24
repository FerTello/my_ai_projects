# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

# Install Pillow and uncomment this line to access image processing.
from PIL import Image, ImageChops, ImageFilter
import numpy as np


class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        pass

    # The primary method for solving incoming Raven's Progressive Matrices.
    # For each problem, your Agent's Solve() method will be called. At the
    # conclusion of Solve(), your Agent should return an int representing its
    # answer to the question: 1, 2, 3, 4, 5, or 6. Strings of these ints 
    # are also the Names of the individual RavensFigures, obtained through
    # RavensFigure.getName(). Return a negative number to skip a problem.
    #
    # Make sure to return your answer *as an integer* at the end of Solve().
    # Returning your answer as a string may cause your program to crash.
    def Solve(self, problem):
        answer = -1

        def select_answer_within_diff_threshold(fig1, fig2, solution_array):
            diff_12 = calc_img_difference(fig1, fig2)
            for i, sol in enumerate(solution_array):
                diff_23 = calc_img_difference(fig2, sol)
                diff_percentage = abs(diff_12 * 100 / diff_23 - 100)
                if are_different(diff_percentage) is False:
                    return i + 1

        def select_answer_within_smallest_diff(fig1, fig2, solution_array):
            diff_12 = calc_img_difference(fig1, fig2)
            diff_percentage = []
            for i, sol in enumerate(solution_array):
                diff_23 = calc_img_difference(fig2, sol)
                diff_percentage.append(abs(diff_12 * 100 / diff_23 - 100))
            return diff_percentage.index(min(diff_percentage)) + 1

        def select_answer_with_addition(fig, added_black_pixels, solution_array):
            for i, sol in enumerate(solution_array):
                H_blacks = calc_black_pixels(fig)
                if calc_black_pixels(sol) == H_blacks + added_black_pixels:
                    return i + 1
            return -1

        def select_answer_similar_to(fig, solution_array):
            diffs_array = []
            for i, sol in enumerate(solution_array):
                diff_np = calc_np_diff(fig, sol)
                diffs_array.append(np.count_nonzero(diff_np))
            return diffs_array.index(min(diffs_array)) + 1

        def is_rotated(origin_fig, end_fig):
            rotated_im = origin_fig.rotate(270)
            # rotate_im.show()
            if rotated_im == end_fig:
                return True
            else:
                return False

        def select_rotated_answer(rotationFrom, solution_array):
            rotated_im = rotationFrom.rotate(270)
            rotated_im.show()
            for i, sol in enumerate(solution_array):
                diff = ImageChops.difference(rotated_im, sol)
                if not diff.getbbox():
                    return i + 1

        def find_transformation(all_figs):
            h0_diff, h1_diff, h2_diff = calc_horizontals_differences(all_figs)
            h0_adds, h1_adds, h2_adds, blacks_counts = has_additions(all_figs)
            if h0_diff == h1_diff == h2_diff == True:
                if h0_adds == h1_adds == h2_adds == True:
                    return 'constant additions', blacks_counts
                elif check_halves_additions(all_figs):
                    return 'halves additions', blacks_counts
            else:
                return 'no horizontal differences', blacks_counts

        def calc_horizontals_differences(all_figs):
            h0_diff = h1_diff = h2_diff = False
            A2B_diff = calc_np_diff(all_figs[0], all_figs[1])
            B2C_diff = calc_np_diff(all_figs[1], all_figs[2])
            D2E_diff = calc_np_diff(all_figs[3], all_figs[4])
            E2F_diff = calc_np_diff(all_figs[4], all_figs[5])
            G2H_diff = calc_np_diff(all_figs[6], all_figs[7])
            if np.count_nonzero(A2B_diff) > 52:
                if np.count_nonzero(B2C_diff) > 52:
                    h0_diff = True
            if np.count_nonzero(D2E_diff) > 52:
                if np.count_nonzero(E2F_diff) > 52:
                    h1_diff = True
            if np.count_nonzero(G2H_diff) > 52:
                h2_diff = True
            return h0_diff, h1_diff, h2_diff


        def check_halves_additions(all_figs):
            check_horizontal_halves(all_figs[0], all_figs[1], all_figs[2])
            check_horizontal_halves(all_figs[3], all_figs[4], all_figs[5])
            return True

        def check_horizontal_halves(fig1, fig2, fig3):
            two_halves_arr = fig1
            for j, y_val in enumerate(fig1):
                for i, x_val in enumerate(y_val):
                    if x_val > fig2[j][i]:
                        two_halves_arr[j][i] = fig2[j][i]
            compare = two_halves_arr == fig3
            if compare.all():
                return True

        def has_additions(all_figs):
            A2B = B2C = D2E = E2F = G2H = h0 = h1 = h2 = False
            A_blacks = calc_black_pixels(all_figs[0])
            B_blacks = calc_black_pixels(all_figs[1])
            C_blacks = calc_black_pixels(all_figs[2])
            D_blacks = calc_black_pixels(all_figs[3])
            E_blacks = calc_black_pixels(all_figs[4])
            F_blacks = calc_black_pixels(all_figs[5])
            G_blacks = calc_black_pixels(all_figs[6])
            H_blacks = calc_black_pixels(all_figs[7])
            blacks_counts = np.zeros((3,3))
            blacks_counts[0] = [A_blacks, B_blacks, C_blacks]
            blacks_counts[1] = [D_blacks, E_blacks, F_blacks]
            blacks_counts[2] = [G_blacks, H_blacks, 0]
            if A_blacks < B_blacks:
                A2B = True
                if B_blacks < C_blacks:
                    B2C = True
            if D_blacks < E_blacks:
                D2E = True
                if E_blacks < F_blacks:
                    E2F = True
            if G_blacks < H_blacks:
                G2H = True
            if A2B == True and B2C == True:
                h0 = True
            if D2E == True and E2F == True:
                h1 = True
            if G2H == True:
                h2 = True
            return h0, h1, h2, blacks_counts

        def calc_pix_increments(black_counts):
            h0_inc_sign = h1_inc_sign = v0_inc_sign = v1_inc_sign = 'positive'
            last_inc = 0
            patterns_arr= np.diff(black_counts)
            for inc in patterns_arr[0,:]:
                if inc < 0:
                    h0_inc_sign = 'negative'
            for inc in patterns_arr[1,:]:
                if inc < 0:
                    h1_inc_sign = 'negative'
            for inc in patterns_arr[:,0]:
                if inc < 0:
                    v0_inc_sign = 'negative'
                last_inc = inc
            for inc in patterns_arr[0:2,1]:
                if inc < 0:
                    v1_inc_sign = 'negative'
            if h0_inc_sign == h1_inc_sign == v0_inc_sign == v1_inc_sign == 'positive':
                return last_inc

        def is_size_increased(diff_12, diff_23):
            # calc_black_pixels()
            pass

        def is_line_transformed(fig1, fig2, fig3):
            diff_12 = calc_img_difference(fig1, fig2)
            diff_23 = calc_img_difference(fig2, fig3)
            if diff_12 != 0 and diff_23 != 0:
                return True, diff_12, diff_23
            else:
                return False, diff_12, diff_23

        def are_different(diff_percentage):
            if diff_percentage > 5:
                return True
            else:
                return False

        def calc_img_difference(file1, file2):
            return np.abs(file1 - file2).sum()

        def calc_np_diff(a,b):
            return abs(a - b)

        def calc_black_pixels(fig):
            return np.count_nonzero(fig == 0)

        def threshold(array):
            # check type numpy
            if type(array) is np.ndarray:
                # Creates a copy to not mess with original
                array = array.copy()
                # set all values below threshold to 0
                array = np.where(array <= 195, 0, 255)
                return array
            else:
                raise Exception("Array must be a numpy array")

        if problem.problemType == '2x2':
            figA = Image.open(problem.figures["A"].visualFilename).convert('L')
            figB = Image.open(problem.figures["B"].visualFilename).convert('L')
            figC = Image.open(problem.figures["C"].visualFilename).convert('L')
            sol1 = Image.open(problem.figures["1"].visualFilename).convert('L')
            sol2 = Image.open(problem.figures["2"].visualFilename).convert('L')
            sol3 = Image.open(problem.figures["3"].visualFilename).convert('L')
            sol4 = Image.open(problem.figures["4"].visualFilename).convert('L')
            sol5 = Image.open(problem.figures["5"].visualFilename).convert('L')
            sol6 = Image.open(problem.figures["6"].visualFilename).convert('L')
            solution_figures = [sol1, sol2, sol3, sol4, sol5, sol6]
            if figA == figB:  # if A == B, then C = D
                # answer = select_answer_within_diff_threshold(figC, solution_figures)
                pass
            else:
                if is_rotated(figA, figB):
                    pass
                    # answer = select_rotated_answer(figA, figB)
        elif problem.problemType == '3x3':
            # if problem.name == 'Basic Problem E-01':
                figA = Image.open(problem.figures["A"].visualFilename).convert('L').filter(ImageFilter.SHARPEN)
                figB = Image.open(problem.figures["B"].visualFilename).convert('L').filter(ImageFilter.SHARPEN)
                figC = Image.open(problem.figures["C"].visualFilename).convert('L').filter(ImageFilter.SHARPEN)
                figD = Image.open(problem.figures["D"].visualFilename).convert('L').filter(ImageFilter.SHARPEN)
                figE = Image.open(problem.figures["E"].visualFilename).convert('L').filter(ImageFilter.SHARPEN)
                figF = Image.open(problem.figures["F"].visualFilename).convert('L').filter(ImageFilter.SHARPEN)
                figG = Image.open(problem.figures["G"].visualFilename).convert('L').filter(ImageFilter.SHARPEN)
                figH = Image.open(problem.figures["H"].visualFilename).convert('L').filter(ImageFilter.SHARPEN)
                sol1 = Image.open(problem.figures["1"].visualFilename).convert('L').filter(ImageFilter.SHARPEN)
                sol2 = Image.open(problem.figures["2"].visualFilename).convert('L').filter(ImageFilter.SHARPEN)
                sol3 = Image.open(problem.figures["3"].visualFilename).convert('L').filter(ImageFilter.SHARPEN)
                sol4 = Image.open(problem.figures["4"].visualFilename).convert('L').filter(ImageFilter.SHARPEN)
                sol5 = Image.open(problem.figures["5"].visualFilename).convert('L').filter(ImageFilter.SHARPEN)
                sol6 = Image.open(problem.figures["6"].visualFilename).convert('L').filter(ImageFilter.SHARPEN)
                sol7 = Image.open(problem.figures["7"].visualFilename).convert('L').filter(ImageFilter.SHARPEN)
                sol8 = Image.open(problem.figures["8"].visualFilename).convert('L').filter(ImageFilter.SHARPEN)

                all_figures_array = [figA, figB, figC, figD, figE, figF, figG, figH, sol1, sol2, sol3, sol4, sol5, sol6, sol7, sol8]

                figs_array = [None]*16
                for i, f in enumerate(all_figures_array):
                    figs_array[i] = np.array(f.resize((32, 32))) #, resample=Image.BICUBIC)) # .astype(np.int)

                th_array = [None]*16
                for i, f in enumerate(figs_array):
                    th_array[i] = threshold(f)

                solutions_array = [None]*8
                for i, f in enumerate(th_array):
                    if i > 7:
                        solutions_array[i - 8] = f

                horizontal_0 = is_line_transformed(th_array[0], th_array[1], th_array[2])
                horizontal_1 = is_line_transformed(th_array[3], th_array[4], th_array[5])

                if horizontal_0[0] is False:
                    if horizontal_1[0] is False:
                        tmp_answer = select_answer_within_diff_threshold(th_array[6], th_array[7], solutions_array) # answer with diff similar to GH
                        if tmp_answer is not None:
                            answer = tmp_answer
                        else:
                            answer = select_answer_within_smallest_diff(th_array[5], th_array[7], solutions_array)
                else:
                    transformation, black_pixels = find_transformation(th_array)
                    if transformation == 'constant additions':
                        pixel_inc = calc_pix_increments(black_pixels)
                        answer = select_answer_with_addition(th_array[7], pixel_inc, solutions_array)
                    elif transformation == 'halves additions':
                        print('halves additions', problem.name)
                    elif transformation == 'no horizontal differences':
                        answer = select_answer_similar_to(th_array[7], solutions_array)


        print(answer)
        return int(answer)