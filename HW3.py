import sys

#class for reviewer objects
class reviewer:
	def __init__(self, ID, cost, prob_right, prob_false_positive):
		self.ID = ID
		self.cost = cost
		self.prob_right = prob_right
		self.prob_false_positive = prob_false_positive

# function figures out the utility of publishing
# also all of the i's are for my debugging (print the actual tree) didn't bother taking them out
def pub_chance_node(prob_succ,revs_used,i):
	cost = 0
	for rev in revs_used:
		cost += rev.cost
	s_util = Succ_util - cost
	f_util = Fail_util - cost
	util = s_util*prob_succ + f_util*(1-prob_succ)

	return util


# Function figures out the expected value of the chance node based on Bayes' Probability
def rev_chance_node(rev,revs,revs_used,prob_succ,instructions,i):
	p_succ_given_yes = (rev.prob_right*prob_succ)/(rev.prob_right*prob_succ+rev.prob_false_positive*(1-prob_succ))
	p_succ_given_no = ((1-rev.prob_right)*prob_succ)/((1-rev.prob_right)*prob_succ+(1-rev.prob_false_positive)*(1-prob_succ))

	yes_instructions = []
	util_yes = choice_node(revs,revs_used,p_succ_given_yes,yes_instructions,i+1)
	no_instructions = []
	util_no = choice_node(revs,revs_used,p_succ_given_no,no_instructions,i+1)

	prob_yes = (rev.prob_right*prob_succ+rev.prob_false_positive*(1-prob_succ))
	prob_no = 1 - prob_yes

	util = util_yes*prob_yes + util_no*prob_no

	instructions.append(yes_instructions)
	instructions.append(no_instructions)

	return util


# Function figures out the chance node with highest expected value,
#  also the if statement in the beginning checks if there's revieweres left,
#  if not decides whether to publish or reject with available information
def choice_node(revs,revs_used,prob_succ,instructions,i):
	if not revs:
		publish = pub_chance_node(prob_succ,revs_used,i+1)
		reject = 0
		for rev in revs_used:
			reject -= rev.cost
		if publish > reject:
			instructions.append('P')
			return publish
		else:
			instructions.append('R')
			return reject

	#Finds greatest util out of the possible reviewers
	best = -100000000
	for x in range(0,len(revs)):
		r = revs.pop(x)
		revs_used.append(r)
		chance_instructions = []
		val = rev_chance_node(r,revs,revs_used,prob_succ,chance_instructions,i+1)
		revs_used.remove(r)
		revs.insert(x,r)
		if val > best:
			best = val
			best_r = r.ID
			best_instructions = chance_instructions

	publish_util = pub_chance_node(prob_succ,revs_used,i+1)
	reject_util = 0 
	for rev in revs_used:
		reject_util -= rev.cost

	#Compare all the available utils
	if best <= reject_util and publish_util <= reject_util:
		#Should do nothing, reject
		instructions.append('R')
		cost = 0
		for rev in revs_used:
			cost += rev.cost
		return (-1*cost)
	elif best > publish_util:
		# Should get it reviewed by the best util reviewer
		instructions.append(str(best_r))
		instructions.append(best_instructions[0])
		instructions.append(best_instructions[1])
		return best
	else:
		#Should publish
		instructions.append('P')
		return publish_util





filename = sys.argv[1]
raw = open(filename,"r")

#Input file parse
i = 0
R = -1
Succ_util = 0
Fail_util = 0
Prob_succ = 0
reviewers = []
for line in raw:
	sline = line.split()
	if i == 0:
		R = int(sline[0])
		Succ_util = int(sline[1])
		Fail_util = int(sline[2])
		Prob_succ = float(sline[3])
		i +=1
	else:
		reviewers.append(reviewer(i,int(sline[0]), float(sline[1]), float(sline[2])))
		i +=1

#Error check
if R != len(reviewers):
	print ("Error: R != #reviewers")
	sys.exit()

instructions = []

util = choice_node(reviewers,[],Prob_succ,instructions,0)

print('Expected Value: ' + str(int(util)))
#print(instructions)


#Interactive part with system user
while (True):
	if instructions[0] == 'P':
		print("Publish")
		break
	elif instructions[0] == 'R':
		print('Reject')
		break
	else:
		s = 'Consult reviewer ' + instructions[0] + ': '
		user_input = input(s)
		if user_input == 'Yes' or user_input == 'yes':
			instructions = instructions[1]
		elif user_input == 'No' or user_input == 'no':
			instructions = instructions[2]
		elif user_input == '0':
			break
		else:
			print('Invalid input, use Yes or No followed by enter, w/out spaces')
			print('Try again, or input 0 for system stop')





















