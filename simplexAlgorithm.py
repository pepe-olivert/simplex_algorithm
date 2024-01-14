import numpy as np

class SimplexAlg():
    """
    Class for applying the simplex algorithm to a concrete instance/problem.
    
    """
    def __init__(self,rows,mode):
        """
        Constructor of the class where we recieve two different arguments, rows, that represent the matrix you build
        before applying the simplex algorithm by hand, and mode, that can take two values, 'max' or 'min'.

        :param rows: List of lists representing the matrix.
        :type rows: np.array(dtype=float)
        :param mode: String representing the mode of the objective function.
        :type mode: str
        """
        ## TODO: BUILD THE REDUCED COST ROW GIVEN A REPRESENTATION OF THE OBJECTIVE FUNCTION
        self.rows = rows
        self.mode = mode
        self.columns = self.get_cols()
        

    def get_cols(self):
        """
        Function that computes the columns from the matrix given the rows.

        :return: List of the columns
        :rtype: List
        """
        c1,c2,c3=[],[],[]
        for r in self.rows:
            c1.append(r[0])
            c2.append(r[1])
            c3.append(r[2])
        c1 = np.array(c1,dtype=float)
        c2=np.array(c2,dtype=float)
        c3=np.array(c3,dtype=float)
        return [c1,c2,c3] 

    def is_simplex_needed(self,r4):
        """
        Auxiliar function to see if there are still reduced costs in the problem and we need to keep
        applying the algorithm.

        :param r4: Last row of the matrix that represents the reduced costs of the problem.
        :type r4: np.array(dtype=float)
        :return: if true is that we still need to apply the simplex algorithm.
        :rtype: bool
        """
        answer=True
        if self.mode == 'max': answer =all(x>=0 for x in r4)
        else: answer =all(x<=0 for x in r4)

        return answer  
    
    def get_max_min_reduced_cost(self,r4):
        """
        Function to select the column that enters the basis.

        :param r4: Last row of the matrix that represents the reduced costs of the problem. If the mode is 'max'we will look for the minimum reduced cost, if it is 'min', viceversa.
        :type r4: np.array(dtype=float)
        :return: tuple indicated the column and its index.
        :rtype: tuple
        """
        selected = (0,r4[0])
        for i,v in enumerate(r4):
            if self.mode == 'max':
                if v < selected[1]: selected = (i,v)
                else: pass

            if self.mode == 'min':
                if v > selected[1]: selected = (i,v)
                else: pass
        return selected
    
    def get_min_division_row(self,selected):
        """
        Select the row to start the algorithm given the column selected to enter the basis. This will mean the change 
        in the matrix by the row named Si into Xi, Xi corresponding to the column that have entered the basis.

        :param selected: Tuple where the column and its index is collected.
        :type selected: tuple
        :return: Tuple indicating the row selected to start applying the simplex.
        :rtype: tuple
        """
        chosen = (0,100000)
        c=selected[0]
        for i,r in enumerate(self.rows):
            
            if r[c]>0 and i != 3:
                n = r[-1]/r[c]
                
                if n<chosen[1]: chosen=(i,n)
        

        return chosen
    
    def transform_all_rows(self,new_row,position):
        """
        Function to compute the different operations in the different rows for the alorithm
        purpose.

        :param new_row: The row that has entered the basis with a 1 in the column selected.
        :type new_row: np.array(dtype=float)
        :return: List of the different 'new' rows.
        :rtype: List
        """
        operator = 0
        new_rows = []
        for r in self.rows:
            operator = r[position[0]]
            new_rows.append(r-operator*new_row)
        return new_rows
    
    def run(self):
        """
        Function that runs the algorithm. Please for further information refer to README.md

        :return: List of the rows when we get to the optimal solution.
        :rtype: List
        """
        r4 = self.rows[-1]
        needed = self.is_simplex_needed(r4)
        while needed==False:
            c_selected = self.get_max_min_reduced_cost(r4)
            r_selected=self.get_min_division_row(c_selected)
            position = (c_selected[0],r_selected[0])
            row = self.rows[position[1]]
            self.rows.pop(position[1])

            # TRANSFORM THE ROW ITSELF
            if row[position[0]]==1:new_row_selected=row
            else:
            
                new_row_selected = row / row[position[0]]
                
            
            
            # TRANSFORM THE REST OF THE ROWS
            self.rows = self.transform_all_rows(new_row_selected,position)
            
            self.rows.insert(position[1],new_row_selected)
            c1,c2,c3 = self.get_cols()
            self.columns = [c1,c2,c3]
            r4 = self.rows[-1]
            needed=self.is_simplex_needed(r4)

        return self.rows


if __name__:
    r1 = np.array([1,2,3/2,1,0,0,12000],dtype=float)
    r2= np.array([2/3,2/3,1,0,1,0,4600],dtype=float)
    r3 = np.array([1/2,1/3,1/2,0,0,1,2400],dtype=float)
    r4=np.array([-11,-16,-15,0,0,0,0],dtype=float)
    rows = [r1,r2,r3,r4] 
    simplex_instance = SimplexAlg(rows,'max')
    print(simplex_instance.run())