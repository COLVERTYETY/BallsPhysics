import unittest
import balls

class testballs(unittest.TestCase):

    def setUp(self):
        pass

    def test_rpopulate(self):
        balls.ball.theballs=[]
        for i in range(10):
            balls.ball.rpopulate(i)
        self.assertEqual(len(balls.ball.theballs),45)
        for i in balls.ball.theballs:
            k=0
            for j in balls.ball.theballs:
                if i==j:
                    k+=1
            self.assertEqual(k,1)
    def test_forces(self):
        balls.ball.theballs=[]
        balls.ball.rpopulate(100)
        for i in balls.ball.theballs:
            i.x=0
            i.y=0
        balls.ball.checkforapplied(0,0)
        for i in balls.ball.theballs:
            self.assertTrue(i.applied)
        balls.ball.checkforletgo(100,100)
        for i in balls.ball.selectedarray:
            self.assertFalse(i.applied)
        for i in balls.ball.theballs:
            self.assertEqual(round(i.ax,2),round(100/balls.ball.COEF,2))
            self.assertEqual(round(i.ay,2),round(100/balls.ball.COEF,2))
            i.apply()
            self.assertEqual(round(i.vx,2),round(100/balls.ball.COEF,2))
            self.assertEqual(round(i.vy,2),round(100/balls.ball.COEF,2))
    def test_carry(self):
        balls.ball.theballs=[]
        balls.ball.rpopulate(10)
        for i in balls.ball.theballs:
            i.x=0
            i.y=0
        balls.ball.checkpickup(0,0)
        balls.ball.checkforcarried(100,100)
        balls.ball.putback()
        for i in balls.ball.theballs:
            self.assertEqual(i.x,i.y)
            self.assertEqual(i.x,100)
if __name__ == '__main__':
    unittest.main()