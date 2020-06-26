import json
from snflambda import snf
from smithnormalform import matrix, snfproblem, z


event_mock_filename = 'data/lambda-event-mock.json'


def test_1x1_z():
    requestBody = {
                    "type": "problem",
                    "ring": "z",
                    "height": 1,
                    "width": 1,
                    "contents": [1]
                  }

    with open(event_mock_filename, 'r') as f:
        f_contents = f.read()

    eventObj = json.loads(f_contents)
    eventObj['body'] = json.dumps(requestBody)
    eventObj['isBase64Encoded'] = False

    result = snf.snf_handler(eventObj, None)

    assert(result['statusCode'] == 200)

    resultBody = json.loads(result['body'])

    assert(resultBody['height'] == 1)
    assert(resultBody['width'] == 1)

    for m in ['A', 'J', 'S', 'T']:
        assert(len(resultBody[m]) == 1)
        assert(resultBody[m][0] == '1')


def test_2x2_z():
    requestBody = {
                   "type": "problem",
                   "ring": "z",
                   "height": 2,
                   "width": 2,
                   "contents": [1, 2, 3, 4]
                  }

    with open(event_mock_filename, 'r') as f:
        f_contents = f.read()

    eventObj = json.loads(f_contents)
    eventObj['body'] = json.dumps(requestBody)
    eventObj['isBase64Encoded'] = False

    result = snf.snf_handler(eventObj, None)

    assert(result['statusCode'] == 200)

    resultBody = json.loads(result['body'])

    assert(resultBody['height'] == 2)
    assert(resultBody['width'] == 2)

    m = matrix.Matrix(2, 2, [z.Z(1), z.Z(2), z.Z(3), z.Z(4)])
    prob = snfproblem.SNFProblem(m)
    prob.computeSNF()

    for i in range(4):
        assert(str(prob.A.elements[i]) == resultBody['A'][i])
        assert(str(prob.J.elements[i]) == resultBody['J'][i])
        assert(str(prob.S.elements[i]) == resultBody['S'][i])
        assert(str(prob.T.elements[i]) == resultBody['T'][i])
