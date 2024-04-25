GRAMMAR = r"""
?start: action
action: operation done | operation join action | followup done
operation: explanation | filter | predictions | whatami | lastturnfilter | lastturnop | data | impfeatures | show | whatif | likelihood | modeldescription | function | score | ndatapoints | interact | label | mistakes | fstats | define | labelfilter | predfilter | numops | getops | numnodes | numfeatures | getfeatures | commonfeatures | getexpr | getcommon | plotpareto | plotsubtree | deletenode | modnode | select | simp | out

labelfilter: " labelfilter" class
predfilter: " predictionfilter" class

numops: " opsnum"
getops: " opsget"
numnodes: " nodesnum"
numfeatures: "featuresnum"
getfeatures: " featuresget"
commonfeatures: " featurescommon"
getexpr: " exprget"
getcommon: " commonget"
plotpareto: " paretoplot"
plotsubtree: " subtreeplot"
deletenode: " nodedelete" nodenumber
modnode: " nodemod" nodenumber math_expression
simp: " simplify"
out: " outlier" (nodenumber)?

nodenumber: " 0" | " 1" | " 2" | " 3" | " 4" | " 5" | " 6" | " 7" | " 8" | " 9" | " 10" | " 11" | " 12" | " 13" | " 14" | " 15" | " 16" | " 17" | " 18" | " 19" | " 20" | " 21" | " 22" | " 23" | " 24" | " 25" | " 26" | " 27" | " 28" | " 29" | " 30" | " 31" | " 32" | " 33" | " 34" | " 35" | " 36" | " 37" | " 38" | " 39" | " 40" | " 41" | " 42" | " 43" | " 44" | " 45" | " 46" | " 47" | " 48" | " 49" | " 50" | " 51" | " 52" | " 53" | " 54" | " 55" | " 56" | " 57" | " 58" | " 59" | " 60" | " 61" | " 62" | " 63" | " 64" | " 65" | " 66" | " 67" | " 68" | " 69" | " 70" | " 71" | " 72" | " 73" | " 74" | " 75" | " 76" | " 77" | " 78" | " 79" | " 80" | " 81" | " 82" | " 83" | " 84" | " 85" | " 86" | " 87" | " 88" | " 89" | " 90" | " 91" | " 92" | " 93" | " 94" | " 95" | " 96" | " 97" | " 98" | " 99" | " 100"

math_expression: term(operator(term))*
term: digit+
operator: add | sub | mul | div
digit: "0"| "1" | "2" | "4" | "5" | "6" | "7" | "8" | "9" | " 3"
add: "+"
sub: "-"
mul: "*"
div: "/"
multops: (ops)+
ops: " +" | " -" | " *" | " /"

selectword: " select"
select: selectword (numoptions equality nodenumber | " model" nodenumber | " selectop" operator || " all")

numoptions: " selectoperators" | " selectnodes" | " selectconstants" | " selectfeatures" | " selectacurracy" | " selectcomplex"

fstats: fstatsword (allfeaturenames | " target")
fstatsword: " statistic"

define: defineword allfeaturenames
defineword: " define"

ndatapoints: " countdata"

mistakes: mistakesword mistakestypes
mistakesword: " mistake"
mistakestypes: " typical" | " count" | " sample"

correct: correctword correcttypes
correctword: " correct"
correcttypes: " typical" | " count" | " sample"

label: " label"

join: and | or
and: " and"
or: " or"
filterword: " filter"

filter: filterword featuretype
featuretype: {avaliablefeaturetypes}

explanation: explainword explaintype
explainword: " explain"
explaintype: featureimportance | lime | cfe
featureimportance: " features"
lime: " lime"
cfe: " cfe"

predictions: " predict"

whatami: " self"

interact: " interact"

data: " data"
modeldescription: " model"
function: " function"

score: scoreword metricword
scoreword: " score"
metricword: " default" | " accuracy" | " f1" | " roc" | " precision" | " recall" | " sensitivity" | " specificity" | " ppv" | " npv"
testword: " test"

followup: " followup"

whatif: whatifword ( ( numfeaturenames numupdates adhocnumvalues ) | catnames )
whatifword: " change"

show: " show"

likelihood: likelihoodword
likelihoodword: " likelihood"

lastturnfilter: " previousfilter"
lastturnop: " previousoperation"

impfeatures: impfeaturesword (allfeaturenames | allfeaturesword | topk)
allfeaturesword: " all"
topk: topkword ( {topkvalues} )
topkword: " topk"


impfeaturesword: " important"
numupdates: " increase" | " set" | " decrease"

done: " [e]"
"""  # noqa: E501

# append the cat feature name and
# the values in another nonterminal
CAT_FEATURES = r"""
catnames: {catfeaturenames}
"""

TARGET_VAR = r"""
class: {classes}
"""

# numfeaturenames are the numerical feature names
# and numvalues are the potential numeric values
NUM_FEATURES = r"""
numnames: {numfeaturenames}
equality: gt | lt | gte | lte | eq | ne
gt: " greater than"
gte: " greater equal than"
lt: " less than"
lte: " less equal than"
eq: " equal to"
ne: " not equal to"
"""

