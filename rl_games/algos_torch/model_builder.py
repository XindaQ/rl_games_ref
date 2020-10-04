from rl_games.common import object_factory
import rl_games.algos_torch
from rl_games.algos_torch import network_builder
from rl_games.algos_torch import models


class ModelBuilder:
    def __init__(self):

        self.model_factory = object_factory.ObjectFactory()
        self.model_factory.register_builder('discrete_a2c', lambda network, **kwargs : models.ModelA2C(network))
        #self.model_factory.register_builder('discrete_a2c_lstm', lambda network, **kwargs : models.LSTMModelA2C(network))
        self.model_factory.register_builder('continuous_a2c', lambda network, **kwargs : models.ModelA2CContinuous(network))
        self.model_factory.register_builder('continuous_a2c_logstd', lambda network, **kwargs : models.ModelA2CContinuousLogStd(network))
        #self.model_factory.register_builder('continuous_a2c_lstm', lambda network, **kwargs : models.LSTMModelA2CContinuous(network))
        #self.model_factory.register_builder('continuous_a2c_lstm_logstd', lambda network, **kwargs : models.LSTMModelA2CContinuousLogStd(network))
        #self.model_factory.register_builder('dqn', lambda network, **kwargs : models.AtariDQN(network))

        self.network_factory = object_factory.ObjectFactory()
        self.network_factory.register_builder('actor_critic', lambda **kwargs : network_builder.A2CBuilder())
        self.network_factory.register_builder('resnet_actor_critic', lambda **kwargs : network_builder.A2CResnetBuilder())
        self.network_factory.register_builder('rnd_curiosity', lambda **kwargs : network_builder.RNDCuriosityBuilder())

        from rl_games.envs.connect4_network import ConnectBuilder
        self.network_factory.register_builder('connect4net', lambda **kwargs : ConnectBuilder())

    def load(self, params):
        self.model_name = params['model']['name']
        self.network_name = params['network']['name']

        network = self.network_factory.create(self.network_name)
        network.load(params['network'])
        model = self.model_factory.create(self.model_name, network=network)

        return model