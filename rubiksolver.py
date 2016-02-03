#Documentation for Rubik's solver

#In this file we specify the effect of each face turn on a 3x3x3 cube and give a solving algorithm
#Later will add computer vision functionality to automatically read state of scrambled cube from photos

#Cube representation: we represent the cube by an array cube[6][3][3] where first index covers the faces, second and third index cover the cubies
#Array is filled with entries 0,1,2,3,4,5 representing the 6 face colours
#Convention on cube orientation and numbering:
#UP, DOWN, LEFT, RIGHT, FRONT, BACK
#Hold cube so that ULF corner is closet to you
#U=cube[0] with first 3-index giving the rows and second 3-index the columns from this view
#L=cube[1] and F=cube[2] with subsidiary indices as above
#Rotate the cube a half turn about UD axis so that URB corner faces
#R=cube[3] and B=cube[4] with subsidiary indices as above
#Finally, rotate the cube so that F is in front, L is left, etc. Then perform a quarter turn around LR axis so D faces
#D=cube[5] with subsidiary indices as above

#Sanity check on numbering convention: here are the indices for the 8 corners

#ULF=cube[0][2][0]=cube[1][0][2]=cube[2][0][0]
#UFR=cube[0][2][2]=cube[2][0][2]=cube[3][0][0]
#URB=cube[0][0][2]=cube[3][0][2]=cube[4][0][0]
#UBL=cube[0][0][0]=cube[4][0][2]=cube[1][0][0]
#FLD=cube[2][2][0]=cube[1][2][2]=cube[5][0][0]
#RFD=cube[3][2][0]=cube[2][2][2]=cube[5][0][2]
#BRD=cube[4][2][0]=cube[3][2][2]=cube[5][2][2]
#LBD=cube[1][2][0]=cube[4][2][2]=cube[5][2][0]

#And for the 12 edges

#UL=cube[0][1][0]=cube[1][0][1]
#UF=cube[0][2][1]=cube[2][0][1]
#UR=cube[0][1][2]=cube[3][0][1]
#UB=cube[0][0][1]=cube[4][0][1]
#LF=cube[1][1][2]=cube[2][1][0]
#FR=cube[2][1][2]=cube[3][1][0]
#RB=cube[3][1][2]=cube[4][1][0]
#BL=cube[4][1][2]=cube[1][1][0]
#LD=cube[1][2][1]=cube[5][1][0]
#FD=cube[2][2][1]=cube[5][0][1]
#RD=cube[3][2][1]=cube[5][1][2]
#BD=cube[4][2][1]=cube[5][2][1]

#Since the centre pieces don't move, we initialise colour choice so that cube[i][1][1] has colour label i for all i

#We now specify the effect of the 6 CLOCKWISE face turns

def Uturn(cube):
    face=0
    #Track the effect of the U turn on the corner pieces

    temp=cube[face][0][0]
    #This part can be copied for each face
    cube[face][0][0]=cube[face][2][0]
    cube[face][2][0]=cube[face][2][2]
    cube[face][2][2]=cube[face][0][2]
    cube[face][0][2]=temp

    temp=cube[1][0][0]

    cube[1][0][0]=cube[2][0][0]
    cube[2][0][0]=cube[3][0][0]
    cube[3][0][0]=cube[4][0][0]
    cube[4][0][0]=temp

    temp=cube[4][0][2]

    cube[4][0][2]=cube[1][0][2]
    cube[1][0][2]=cube[2][0][2]
    cube[2][0][2]=cube[3][0][2]
    cube[3][0][2]=temp

    #Track the effect of the U turn on the edge pieces

    temp=cube[face][1][0]
    #This part can be copied for each face
    cube[face][1][0]=cube[face][2][1]
    cube[face][2][1]=cube[face][1][2]
    cube[face][1][2]=cube[face][0][1]
    cube[face][0][1]=temp

    temp=cube[1][0][1]

    cube[1][0][1]=cube[2][0][1]
    cube[2][0][1]=cube[3][0][1]
    cube[3][0][1]=cube[4][0][1]
    cube[4][0][1]=temp

def Lturn(cube):
    face=1
    #Track the effect of the L turn on the corner pieces

    temp=cube[face][0][0]
    #This part can be copied for each face
    cube[face][0][0]=cube[face][2][0]
    cube[face][2][0]=cube[face][2][2]
    cube[face][2][2]=cube[face][0][2]
    cube[face][0][2]=temp

    temp=cube[4][0][2]

    cube[4][0][2]=cube[5][2][0]
    cube[5][2][0]=cube[2][2][0]
    cube[2][2][0]=cube[0][2][0]
    cube[0][2][0]=temp

    temp=cube[0][0][0]

    cube[0][0][0]=cube[4][2][2]
    cube[4][2][2]=cube[5][0][0]
    cube[5][0][0]=cube[2][0][0]
    cube[2][0][0]=temp

    #Track the effect of the L turn on the edge pieces

    temp=cube[face][1][0]
    #This part can be copied for each face
    cube[face][1][0]=cube[face][2][1]
    cube[face][2][1]=cube[face][1][2]
    cube[face][1][2]=cube[face][0][1]
    cube[face][0][1]=temp

    temp=cube[4][1][2]

    cube[4][1][2]=cube[5][1][0]
    cube[5][1][0]=cube[2][1][0]
    cube[2][1][0]=cube[0][1][0]
    cube[0][1][0]=temp

def Fturn(cube):
    face=2
    #Track the effect of the F turn on the corner pieces

    temp=cube[face][0][0]
    #This part can be copied for each face
    cube[face][0][0]=cube[face][2][0]
    cube[face][2][0]=cube[face][2][2]
    cube[face][2][2]=cube[face][0][2]
    cube[face][0][2]=temp

    temp=cube[1][0][2]

    cube[1][0][2]=cube[5][0][0]
    cube[5][0][0]=cube[3][2][0]
    cube[3][2][0]=cube[0][2][2]
    cube[0][2][2]=temp

    temp=cube[0][2][0]

    cube[0][2][0]=cube[1][2][2]
    cube[1][2][2]=cube[5][0][2]
    cube[5][0][2]=cube[3][0][0]
    cube[3][0][0]=temp

    #Track the effect of the F turn on the edge pieces

    temp=cube[face][1][0]
    #This part can be copied for each face
    cube[face][1][0]=cube[face][2][1]
    cube[face][2][1]=cube[face][1][2]
    cube[face][1][2]=cube[face][0][1]
    cube[face][0][1]=temp

    temp=cube[1][1][2]

    cube[1][1][2]=cube[5][0][1]
    cube[5][0][1]=cube[3][1][0]
    cube[3][1][0]=cube[0][2][1]
    cube[0][2][1]=temp

def Rturn(cube):
    face=3
    #Track the effect of the R turn on the corner pieces

    temp=cube[face][0][0]
    #This part can be copied for each face
    cube[face][0][0]=cube[face][2][0]
    cube[face][2][0]=cube[face][2][2]
    cube[face][2][2]=cube[face][0][2]
    cube[face][0][2]=temp

    temp=cube[2][0][2]

    cube[2][0][2]=cube[5][0][2]
    cube[5][0][2]=cube[4][2][0]
    cube[4][2][0]=cube[0][0][2]
    cube[0][0][2]=temp

    temp=cube[0][2][2]

    cube[0][2][2]=cube[2][2][2]
    cube[2][2][2]=cube[5][2][2]
    cube[5][2][2]=cube[4][0][0]
    cube[4][0][0]=temp

    #Track the effect of the R turn on the edge pieces

    temp=cube[face][1][0]
    #This part can be copied for each face
    cube[face][1][0]=cube[face][2][1]
    cube[face][2][1]=cube[face][1][2]
    cube[face][1][2]=cube[face][0][1]
    cube[face][0][1]=temp

    temp=cube[2][1][2]

    cube[2][1][2]=cube[5][1][2]
    cube[5][1][2]=cube[4][1][0]
    cube[4][1][0]=cube[0][1][2]
    cube[0][1][2]=temp

def Bturn(cube):
    face=4
    #Track the effect of the B turn on the corner pieces

    temp=cube[face][0][0]
    #This part can be copied for each face
    cube[face][0][0]=cube[face][2][0]
    cube[face][2][0]=cube[face][2][2]
    cube[face][2][2]=cube[face][0][2]
    cube[face][0][2]=temp

    temp=cube[3][0][2]

    cube[3][0][2]=cube[5][2][2]
    cube[5][2][2]=cube[1][2][0]
    cube[1][2][0]=cube[0][0][0]
    cube[0][0][0]=temp

    temp=cube[0][0][2]

    cube[0][0][2]=cube[3][2][2]
    cube[3][2][2]=cube[5][2][0]
    cube[5][2][0]=cube[1][0][0]
    cube[1][0][0]=temp

    #Track the effect of the B turn on the edge pieces

    temp=cube[face][1][0]
    #This part can be copied for each face
    cube[face][1][0]=cube[face][2][1]
    cube[face][2][1]=cube[face][1][2]
    cube[face][1][2]=cube[face][0][1]
    cube[face][0][1]=temp

    temp=cube[3][1][2]

    cube[3][1][2]=cube[5][2][1]
    cube[5][2][1]=cube[1][1][0]
    cube[1][1][0]=cube[0][0][1]
    cube[0][0][1]=temp

def Dturn(cube):
    face=5
    #Track the effect of the D turn on the corner pieces

    temp=cube[face][0][0]
    #This part can be copied for each face
    cube[face][0][0]=cube[face][2][0]
    cube[face][2][0]=cube[face][2][2]
    cube[face][2][2]=cube[face][0][2]
    cube[face][0][2]=temp

    temp=cube[1][2][2]

    cube[1][2][2]=cube[4][2][2]
    cube[4][2][2]=cube[3][2][2]
    cube[3][2][2]=cube[2][2][2]
    cube[2][2][2]=temp

    temp=cube[2][2][0]

    cube[2][2][0]=cube[1][2][0]
    cube[1][2][0]=cube[4][2][0]
    cube[4][2][0]=cube[3][2][0]
    cube[3][2][0]=temp

    #Track the effect of the D turn on the edge pieces

    temp=cube[face][1][0]
    #This part can be copied for each face
    cube[face][1][0]=cube[face][2][1]
    cube[face][2][1]=cube[face][1][2]
    cube[face][1][2]=cube[face][0][1]
    cube[face][0][1]=temp

    temp=cube[1][2][1]

    cube[1][2][1]=cube[4][2][1]
    cube[4][2][1]=cube[3][2][1]
    cube[3][2][1]=cube[2][2][1]
    cube[2][2][1]=temp

def turntype(num):
    if num==1:
        return " "
    elif num==2:
        return "2"
    else:
        return "\'"

def name(face):
    if face==0:
        return "blue"
    elif face==1:
        return "orange"
    elif face==2:
        return "white"
    elif face==3:
        return "red"
    elif face==4:
        return "yellow"
    else:
        return "green"

def turn(cube,face,num):
    #num=1, 2, or -1 to represent clockwise, half, or anticlockwise turns of the face
    if num==-1: num=3
    if num==-2: num=2
    if num==-3: num=1
    if num==-4: num=0
    if num==4: num=0
    for n in range(num):
        if n==0:
            print name(face),turntype(num)
        if face==0:
            Uturn(cube)
        elif face==1:
            Lturn(cube)
        elif face==2:
            Fturn(cube)
        elif face==3:
            Rturn(cube)
        elif face==4:
            Bturn(cube)
        else:
            Dturn(cube)

def adjacent(face):
    #Returns the 4 adjacent faces to a given face followed by opposite face as an array of size 5, in the order above, to the left, to the right, below, opposite when face is oriented so subsidiary idices increase down and to the right
    if face==0:
        return [4,1,3,2,5]
    elif face==1:
        return [0,4,2,5,3]
    elif face==2:
        return [0,1,3,5,4]
    elif face==3:
        return [0,2,4,5,1]
    elif face==4:
        return [0,3,1,5,2]
    else:
        return [2,1,3,4,0]

def setcube(cube):
    #Build a setlike dictionary representation of the cubes state
    #Will not use turns on this representation, but will ue to track the position of pieces during the solve more easily

    cubedict=dict()

    cubedict['ULF']=set([cube[0][2][0],cube[1][0][2],cube[2][0][0]])
    cubedict['UFR']=set([cube[0][2][2],cube[2][0][2],cube[3][0][0]])
    cubedict['URB']=set([cube[0][0][2],cube[3][0][2],cube[4][0][0]])
    cubedict['UBL']=set([cube[0][0][0],cube[4][0][2],cube[1][0][0]])
    cubedict['FLD']=set([cube[2][2][0],cube[1][2][2],cube[5][0][0]])
    cubedict['RFD']=set([cube[3][2][0],cube[2][2][2],cube[5][0][2]])
    cubedict['BRD']=set([cube[4][2][0],cube[3][2][2],cube[5][2][2]])
    cubedict['LBD']=set([cube[1][2][0],cube[4][2][2],cube[5][2][0]])

    cubedict['UL']=set([cube[0][1][0],cube[1][0][1]])
    cubedict['UF']=set([cube[0][2][1],cube[2][0][1]])
    cubedict['UR']=set([cube[0][1][2],cube[3][0][1]])
    cubedict['UB']=set([cube[0][0][1],cube[4][0][1]])
    cubedict['LF']=set([cube[1][1][2],cube[2][1][0]])
    cubedict['FR']=set([cube[2][1][2],cube[3][1][0]])
    cubedict['RB']=set([cube[3][1][2],cube[4][1][0]])
    cubedict['BL']=set([cube[4][1][2],cube[1][1][0]])
    cubedict['LD']=set([cube[1][2][1],cube[5][1][0]])
    cubedict['FD']=set([cube[2][2][1],cube[5][0][1]])
    cubedict['RD']=set([cube[3][2][1],cube[5][1][2]])
    cubedict['BD']=set([cube[4][2][1],cube[5][2][1]])

    return cubedict

def piecename(i,j,k):
    #Returns the 2 or 3 character name of cube[i][j][k] in the dictionary keys above

    if (i,j,k)==(0,2,0) or (i,j,k)==(1,0,2) or (i,j,k)==(2,0,0):
        return 'ULF'
    elif (i,j,k)==(0,2,2) or (i,j,k)==(2,0,2) or (i,j,k)==(3,0,0):
        return 'UFR'
    elif (i,j,k)==(0,0,2) or (i,j,k)==(3,0,2) or (i,j,k)==(4,0,0):
        return 'URB'
    elif (i,j,k)==(0,0,0) or (i,j,k)==(4,0,2) or (i,j,k)==(1,0,0):
        return 'UBL'
    elif (i,j,k)==(2,2,0) or (i,j,k)==(1,2,2) or (i,j,k)==(5,0,0):
        return 'FLD'
    elif (i,j,k)==(3,2,0) or (i,j,k)==(2,2,2) or (i,j,k)==(5,0,2):
        return 'RFD'
    elif (i,j,k)==(4,2,0) or (i,j,k)==(3,2,2) or (i,j,k)==(5,2,2):
        return 'BRD'
    elif (i,j,k)==(1,2,0) or (i,j,k)==(4,2,2) or (i,j,k)==(5,2,0):
        return 'LBD'
    elif (i,j,k)==(0,1,0) or (i,j,k)==(1,0,1):
        return 'UL'
    elif (i,j,k)==(0,2,1) or (i,j,k)==(2,0,1):
        return 'UF'
    elif (i,j,k)==(0,1,2) or (i,j,k)==(3,0,1):
        return 'UR'
    elif (i,j,k)==(0,0,1) or (i,j,k)==(4,0,1):
        return 'UB'
    elif (i,j,k)==(1,1,2) or (i,j,k)==(2,1,0):
        return 'LF'
    elif (i,j,k)==(2,1,2) or (i,j,k)==(3,1,0):
        return 'FR'
    elif (i,j,k)==(3,1,2) or (i,j,k)==(4,1,0):
        return 'RB'
    elif (i,j,k)==(4,1,2) or (i,j,k)==(1,1,0):
        return 'BL'
    elif (i,j,k)==(1,2,1) or (i,j,k)==(5,1,0):
        return 'LD'
    elif (i,j,k)==(2,2,1) or (i,j,k)==(5,0,1):
        return 'FD'
    elif (i,j,k)==(3,2,1) or (i,j,k)==(5,1,2):
        return 'RD'
    else:
        return 'BD'

def edgecorrect(cube,face,edge):
    #Determines whether an edge on the cube face is positioned AND oriented correctly
    #Returns 0 if edge is correctly oriented, 1 if edge is correct but flipped, and -1 otherwise
    #Edges are numbered 0,1,2,3 corresponding to subsidiary indices [1][2],[0][1],[1][0],[2][1]
    #Numbering is set up so that turning face edge times puts relevant edge on the right when viewing face on
    adj=adjacent(face)

    if edge==0:
        j=1
        k=2
        a=2
    elif edge==1:
        j=0
        k=1
        a=0
    elif edge==2:
        j=1
        k=0
        a=1
    else:
        j=2
        k=1
        a=3

    name=piecename(face,j,k)
    otherside=(setcube(cube)[name].difference(set([cube[face][j][k]]))).pop()
    if cube[face][j][k]==cube[face][1][1] and otherside==cube[adj[a]][1][1]:
        return 0
    elif cube[face][j][k]==cube[adj[a]][1][1] and otherside==cube[face][1][1]:
        return 1
    else:
        return -1

def cornercorrect(cube,face,corner):
    #Determines whether a corner on the cube face is positioned AND oriented correctly
    #Returns 0 if corner is correctly oriented, 1 if corner is correct but needs to be rotated clockwise, 2 if corner is correct but needs to be rotated anticlockwise, and -1 otherwise
    #Corners are numbered 0,1,2,3 corresponding to subsidiary indices [0][2],[0][0],[2][0],[2][2]
    #Numbering is set up so that turning face corner times puts relevant corner on the top right when viewing face on
    adj=adjacent(face)

    #Here a1 will specify the face one place clockwise of the given face and a2 the face one place anticlockwise

    if corner==0:
        j=0
        k=2
        a1=0
        a2=2
    elif corner==1:
        j=0
        k=0
        a1=1
        a2=0
    elif corner==2:
        j=2
        k=0
        a1=3
        a2=1
    else:
        j=2
        k=2
        a1=2
        a2=3

    name=piecename(face,j,k)
    colours=setcube(cube)[name]
    if colours!=set([cube[face][1][1],cube[adj[a1]][1][1],cube[adj[a2]][1][1]]):
        return -1
    elif cube[face][j][k]==cube[face][1][1]:
        return 0
    elif cube[face][j][k]==cube[adj[a1]][1][1]:
        return 1
    else:
        return 2

def orientcorners(cube,face,c1,c2):
    #Turns c1 clockwise and c2 anticlockwise on a face. Corners are numbered 0,1,2,3 corresponding to subsidiary indices [0][2],[0][0],[2][0],[2][2]
    #Numbering is set up so that turning face c1 times puts relevant corner in top right when viewing face on
    adj=adjacent(face)

    turn(cube,face,c1)

    turn(cube,adj[2],1)
    turn(cube,adj[4],1)
    turn(cube,adj[2],3)
    turn(cube,adj[4],3)
    turn(cube,adj[2],1)
    turn(cube,adj[4],1)
    turn(cube,adj[2],3)

    turn(cube,face,c2-c1)

    turn(cube,adj[2],1)
    turn(cube,adj[4],3)
    turn(cube,adj[2],3)
    turn(cube,adj[4],1)
    turn(cube,adj[2],1)
    turn(cube,adj[4],3)
    turn(cube,adj[2],3)

    turn(cube,face,4-c2)

def orientedges(cube,face,e1,e2):
    #Flips edges e1 and d2 on a face. Edges are numbered 0,1,2,3 corresponding to subsidiary indices [1][2],[0][1],[1][0],[2][1]
    #Numbering is set up so that turning face e1 times puts relevant edge on the right when viewing face on
    adj=adjacent(face)

    turn(cube,face,e1)

    turn(cube,adj[2],1)
    turn(cube,adj[4],1)
    turn(cube,face,3)
    turn(cube,adj[0],1)

    turn(cube,face,e2-e1)

    turn(cube,adj[0],3)
    turn(cube,face,1)
    turn(cube,adj[4],3)
    turn(cube,adj[2],3)

    turn(cube,face,4-e2)

def permuteedges(cube,face,e1,e2,e3):
    #Swaps edges e1 and e2, then edges e3 and e4 on a face. Edges are numbered 0,1,2,3 corresponding to subsidiary indices [1][2],[0][1],[1][0],[2][1]
    #Assume e4-e3=e2-e1
    #Numbering is set up so that turning face e1 times puts relevant edge on the right when viewing face on
    adj=adjacent(face)
    a=[2,0,1,3]

    turn(cube,face,e1)

    turn(cube,adj[2],2)
    turn(cube,adj[4],e2-e1)
    turn(cube,adj[a[e2]],2)
    turn(cube,adj[4],(4-e2+e1)%4)
    turn(cube,adj[2],2)

    turn(cube,face,e3-e1)

    turn(cube,adj[2],2)
    turn(cube,adj[4],e2-e1)
    turn(cube,adj[a[e2]],2)
    turn(cube,adj[4],(4-e2+e1)%4)
    turn(cube,adj[2],2)

    turn(cube,face,4-e3)

def permutecorners(cube,face,c1,c2,c3):
    #Performs the 3 cycle c1->c2->c3->c1 on 3 corners. Corners are numbered 0,1,2,3 corresponding to subsidiary indices [0][2],[0][0],[2][0],[2][2]
    #Numbering is set up so that turning face c1 times puts relevant corner in top right when viewing face on
    #Corners c1 and c2 lie on the face, while c3 lies on the opposite face, with the numbering matching the numbering on the given face
    #Assume c3!=3
    adj=adjacent(face)

    turn(cube,face,c1)

    turn(cube,adj[2],1)
    if c3==0:
        turn(cube,adj[4],1)
    else:
        turn(cube,adj[4],4-c3)
    turn(cube,adj[2],3)

    turn(cube,face,c2-c1)

    turn(cube,adj[2],1)
    if c3==0:
        turn(cube,adj[4],3)
    else:
        turn(cube,adj[4],c3)
    turn(cube,adj[2],3)

    turn(cube,face,4-c2)

def edgepermutation(cube,face):
    #Determines the permutation of edges on a face, assuming all correct edges are already on the face
    #Edges are numbered 0,1,2,3 corresponding to subsidiary indices [1][2],[0][1],[1][0],[2][1] when viewing cube face on
    perm=[0,0,0,0]
    adj=adjacent(face)
    a=[2,0,1,3]
    for edge in range(4):
        if edge==0:
            j=1
            k=2
        elif edge==1:
            j=0
            k=1
        elif edge==2:
            j=1
            k=0
        else:
            j=2
            k=1

        name=piecename(face,j,k)
        othercolour=(setcube(cube)[name].difference(set([cube[face][1][1]]))).pop()
        for otheredge in range(4):
            if othercolour==cube[adj[a[otheredge]]][1][1]:
                perm[edge]=otheredge

    return perm

def permutationtype(perm):
    #Returns the cycle type of a permutation of [0,1,2,3]
    ans=[]
    for i in range(4):
        if i in ans:
            break
        else:
            ans.append(i)
            j=i
            while True:
                j=perm[j]
                if j==i:
                    break
                else:
                    ans.append(j)
            ans.append(' ')
    return ans

def sign(perm):
    #Returns the sign of a permutation
    cycles=permutationtype(perm)
    cyclelength=0
    sign=1
    for x in cycles:
        if x==" ":
            if cyclelength%2==0:
                sign=-sign
            cyclelength=0
        else:
            cyclelength=cyclelength+1
    return sign

def is3cycle(perm):
    #Returns 0 if perm is not a 3 cycle, and otherwise returns the 3 elements of the cycle


#cube=[[[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0]]]

#Sample scrambled state below

cube=[[[3,2,5],[0,0,5],[2,0,3]],[[2,3,0],[1,1,1],[1,1,1]],[[1,4,4],[2,2,1],[4,3,3]],[[0,4,3],[0,3,2],[4,0,5]],[[2,3,0],[5,4,4],[1,3,4]],[[0,4,5],[5,5,2],[5,5,2]]]



while True:
    f=raw_input("Face: ")
    C1=raw_input("e1: ")
    C2=raw_input("e2: ")
    C3=raw_input("e3: ")
    C4=raw_input("e4: ")
    try:
        face=int(f)
        e1=int(C1)
        e2=int(C2)
        e3=int(C3)
        e4=int(C4)
    except:
        break
    permuteedges(cube,face,e1,e2,e3,e4)

for i in range(6):
    print "Face",i
    for j in range(3):
        for k in range(3):
            print cube[i][j][k]
    print "-----"

#Read scrambled state
#Later will replace this with computer vision code but for now manually enter the sticker colours
#for i in range(6):
#    print "Face",i
#    for j in range(3):
#        for k in range(3):
#            cube[i][j][k]=raw_input("C:")
            #cube[i][j][k]=int(cubie)
            #May need above line or similar depending on representation of colours. For now keep as integers. Note that if this changes will need to change the labelling of faces
#    print "-----"

#Solving algorithm implented will be my intuitive/conjugator solver.

#D layer edges

#Decide which face to start on

face=5
correct=0

for i in range(5,-1,-1):
    edgescorrect=0
    for edge in range(4):
        if edgecorrect(cube,i,edge)==0:
            edgescorrect=edgescorrect+1
    if edgescorrect>correct:
        correct=edgescorrect
        face=i

adj=adjacent(face)

#Fix remaining edges on this face

for edge in range(4):
    if edgecorrect(cube,face,edge)==0:
        continue
    elif edgecorrect(cube,face,edge)==1:
        turn(cube,face,edge)
        turn(cube,adj[2],1)
        turn(cube,adj[4],1)
        turn(cube,face,3)
        turn(cube,adj[0],1)
        turn(cube,face,4-edge)
    else:
        pass

        #NEED TO THINK ABOUT CODE HERE

#Middle layer edges

#NEED TO THINK ABOUT CODE HERE

#Permute U layer edges

perm=edgepermutation(cube,adj[4])
if sign(perm)==-1:
    turn(cube,adj[4],1)

perm=edgepermutation(cube,adj[4])
#Edges now require an even permutation to position

#CONTINUE FROM HERE

#Worth considering embedding detecting the permutation required in the sign function

#Orient U layer edges



#Permute corners



#Orient corners



#while True:
#    f=raw_input("Face: ")
#    C=raw_input("edge: ")
#    try:
#        face=int(f)
#        e1=int(C)
#    except:
#        break
#    print edgecorrect(cube,face,e1)

#for i in range(6):
#    print "Face",i
#    for j in range(3):
#        for k in range(3):
#            print cube[i][j][k]
#    print "-----"
