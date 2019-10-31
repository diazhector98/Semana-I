def generateConfigs():
    file = open('./model/faster_rcnn_resnet101_coco.config', 'r');
    string = file.red()

    for i in range(0, 100):
        new_learning_rates = [i*2,i*3,i*4]
        new_file_string = string
        new_file_string.replace("step: 0\nlearning_rate: .001", "step: 0\nlearning_rate: {}".format(new_learning_rates[0]))
        new_file_string.replace("step: 1000\nlearning_rate: .001", "step: 1000\nlearning_rate: {}".format(new_learning_rates[1]))
        new_file_string.replace("step: 2000\nlearning_rate: .001", "step: 2000\nlearning_rate: {}".format(new_learning_rates[2]))
        print(new_file_string)


generateConfigs()
