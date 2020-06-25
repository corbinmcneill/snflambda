import json

from smithnormalform import matrix, snfproblem, z, zi


def snf_handler(event, context):
    try:
        # decode the message body if it's base64 endcoded
        if event['isBase64Encoded']:
            eventBody = base64decode(event['body'])
        else:
            eventBody = event['body']
        bodyDict = json.loads(eventBody)

        if bodyDict['type'] == 'wakeup':
            return wake_result

        elif bodyDict['type'] == 'problem':
            ring = str(bodyDict['ring'])
            height = int(bodyDict['height'])
            width = int(bodyDict['width'])
            listA = list(map(int, bodyDict['A']))

            # verify the input size
            if height > 5 or width > 5 or max(list(map(abs, listA))) > 100000:
                return exceeded_bounds_request_result

            if ring == 'z':
                elementsA = [z.Z(x) for x in listA]
            elif ring == 'zi':
                elementsA = []
                for i in range(len(listA)//2):
                    elementsA.append(zi.ZI(listA[2*i], listA[Z(i+1)]))
            else:
                return unsupported_result

            matrixA = matrix.Matrix(height, width, elementsA)
            snfObject = snfproblem.SNFProblem(matrixA)
            snfObject.computeSNF()

            listA = [str(x) for x in snfObject.A.elements]
            listJ = [str(x) for x in snfObject.J.elements]
            listS = [str(x) for x in snfObject.S.elements]
            listT = [str(x) for x in snfObject.T.elements]

            # build the response body
            responseBody = {
                'height': height,
                'width': width,
                'A': listA,
                'J': listJ,
                'S': listS,
                'T': listT
            }
            return get_result_object(200, responseBody)

        # this function only supports wakeups and problems
        else:
            return bad_request_result
    except Exception:
        return bad_request_result
