class Solution(object):
    def distMoney(self, money, children):

        if money < children:
            return -1
        # each gets 1$ 
        money -= children
        #give as many as possible 7 more since 7+1=8
        count = min(money // 7, children)

        money -= count * 7
        children -= count

        if children == 0 and money > 0:
            return count - 1

        if children == 1 and money == 3:
            return count - 1

        return count