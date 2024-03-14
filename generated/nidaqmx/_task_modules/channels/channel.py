# Do not edit this file; it was automatically generated.

import nidaqmx._task_modules.channels  # circular import: Channel._factory uses derived classes
from nidaqmx.system.physical_channel import _PhysicalChannelAlternateConstructor
from nidaqmx.utils import flatten_channel_string, unflatten_channel_string
from nidaqmx.constants import (
    ChannelType, SyncUnlockBehavior, _Save)


class Channel:
    """
    Represents virtual channel or a list of virtual channels.
    """
    __slots__ = ['_handle', '_name', '_interpreter', '__weakref__']

    def __init__(self, task_handle, virtual_or_physical_name, interpreter):
        """
        Args:
            task_handle (TaskHandle): Specifies the handle of the task that
                this channel is associated with.
            virtual_or_physical_name (str): Specifies the flattened virtual or
                physical name of a channel.
            interpreter (BaseInterpreter): Specifies the interpreter instance.
        """
        self._handle = task_handle
        self._name = virtual_or_physical_name
        self._interpreter = interpreter

    def __add__(self, other):
        if not isinstance(other, self.__class__):
            raise NotImplementedError(
                'Cannot concatenate objects of type {} and {}'
                .format(self.__class__, other.__class__))

        if self._handle != other._handle:
            raise NotImplementedError(
                'Cannot concatenate Channel objects from different tasks.')

        name = flatten_channel_string([self.name, other.name])
        return Channel._factory(self._handle, name, self._interpreter)

    def __contains__(self, item):
        channel_names = self.channel_names

        if isinstance(item, str):
            items = unflatten_channel_string(item)
        elif isinstance(item, Channel):
            items = item.channel_names

        return all([item in channel_names for item in items])

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (self._handle == other._handle and
                    set(self.channel_names) == set(other.channel_names))
        return False

    def __hash__(self):
        return self._interpreter.hash_task_handle(self._handle) ^ hash(frozenset(self.channel_names))

    def __iadd__(self, other):
        return self.__add__(other)

    def __iter__(self):
        for channel_name in self.channel_names:
            yield Channel._factory(self._handle, channel_name, self._interpreter)

    def __len__(self):
        return len(self.channel_names)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __reversed__(self):
        channel_names = self.channel_names
        channel_names.reverse()

        for channel_name in channel_names:
            yield Channel._factory(self._handle, channel_name, self._interpreter)

    def __repr__(self):
        return f'Channel(name={self.name})'

    @staticmethod
    def _factory(task_handle, virtual_or_physical_name, interpreter):
        """
        Implements the factory pattern for nidaqmx channels.

        Args:
            task_handle (TaskHandle): Specifies the handle of the task that
                this channel is associated with.
            virtual_or_physical_name (str): Specifies the flattened virtual
                or physical name of a channel.
            interpreter (BaseInterpreter): Specifies the interpreter instance.
        Returns:
            nidaqmx._task_modules.channels.channel.Channel:

            Indicates an object that represents the specified channel.
        """
        chan_type = interpreter.get_chan_attribute_int32(task_handle, virtual_or_physical_name, 0x187f)

        channel_type = ChannelType(chan_type)

        if channel_type == ChannelType.ANALOG_INPUT:
            return nidaqmx._task_modules.channels.AIChannel(
                task_handle, virtual_or_physical_name, interpreter)
        elif channel_type == ChannelType.ANALOG_OUTPUT:
            return nidaqmx._task_modules.channels.AOChannel(
                task_handle, virtual_or_physical_name, interpreter)
        elif channel_type == ChannelType.COUNTER_INPUT:
            return nidaqmx._task_modules.channels.CIChannel(
                task_handle, virtual_or_physical_name, interpreter)
        elif channel_type == ChannelType.COUNTER_OUTPUT:
            return nidaqmx._task_modules.channels.COChannel(
                task_handle, virtual_or_physical_name, interpreter)
        elif channel_type == ChannelType.DIGITAL_INPUT:
            return nidaqmx._task_modules.channels.DIChannel(
                task_handle, virtual_or_physical_name, interpreter)
        elif channel_type == ChannelType.DIGITAL_OUTPUT:
            return nidaqmx._task_modules.channels.DOChannel(
                task_handle, virtual_or_physical_name, interpreter)

    @property
    def name(self):
        """
        str: Specifies the name of the virtual channel this object
            represents.
        """
        if self._name:
            return self._name
        else:
            return self._all_channels_name

    @property
    def channel_names(self):
        """
        List[str]: Specifies the unflattened list of the virtual channels.
        """
        if self._name:
            return unflatten_channel_string(self._name)
        else:
            return unflatten_channel_string(self._all_channels_name)

    @property
    def _all_channels_name(self):
        """
        str: Specifies the flattened names of all the virtual channels in
            the task.
        """
        val = self._interpreter.get_task_attribute_string(self._handle, 0x1273)
        return val

    @property
    def chan_type(self):
        """
        :class:`nidaqmx.constants.ChannelType`: Indicates the type of
            the virtual channel.
        """

        val = self._interpreter.get_chan_attribute_int32(self._handle, self._name, 0x187f)
        return ChannelType(val)

    @property
    def description(self):
        """
        str: Specifies a user-defined description for the channel.
        """

        val = self._interpreter.get_chan_attribute_string(self._handle, self._name, 0x1926)
        return val

    @description.setter
    def description(self, val):
        self._interpreter.set_chan_attribute_string(self._handle, self._name, 0x1926, val)

    @description.deleter
    def description(self):
        self._interpreter.reset_chan_attribute(self._handle, self._name, 0x1926)

    @property
    def is_global(self):
        """
        bool: Indicates whether the channel is a global channel.
        """

        val = self._interpreter.get_chan_attribute_bool(self._handle, self._name, 0x2304)
        return val

    @property
    def physical_channel(self):
        """
        :class:`nidaqmx.system.physical_channel.PhysicalChannel`:
            Specifies the name of the physical channel upon which this
            virtual channel is based.
        """

        val = self._interpreter.get_chan_attribute_string(self._handle, self._name, 0x18f5)
        return _PhysicalChannelAlternateConstructor(val, self._interpreter)

    @physical_channel.setter
    def physical_channel(self, val):
        val = val.name
        self._interpreter.set_chan_attribute_string(self._handle, self._name, 0x18f5, val)

    @property
    def sync_unlock_behavior(self):
        """
        :class:`nidaqmx.constants.SyncUnlockBehavior`: Specifies the
            action to take if the target loses its synchronization to
            the grand master.
        """

        val = self._interpreter.get_chan_attribute_int32(self._handle, self._name, 0x313c)
        return SyncUnlockBehavior(val)

    @sync_unlock_behavior.setter
    def sync_unlock_behavior(self, val):
        val = val.value
        self._interpreter.set_chan_attribute_int32(self._handle, self._name, 0x313c, val)

    @sync_unlock_behavior.deleter
    def sync_unlock_behavior(self):
        self._interpreter.reset_chan_attribute(self._handle, self._name, 0x313c)

    def save(self, save_as="", author="", overwrite_existing_channel=False,
             allow_interactive_editing=True, allow_interactive_deletion=True):
        """
        Saves this local or global channel to MAX as a global channel.

        Args:
            save_as (Optional[str]): Is the name to save the task,
                global channel, or custom scale as. If you do not
                specify a value for this input, NI-DAQmx uses the name
                currently assigned to the task, global channel, or
                custom scale.
            author (Optional[str]): Is a name to store with the task,
                global channel, or custom scale.
            overwrite_existing_channel (Optional[bool]): Specifies whether to
                overwrite a global channel of the same name if one is already
                saved in MAX. If this input is False and a global channel of
                the same name is already saved in MAX, this function returns
                an error.
            allow_interactive_editing (Optional[bool]): Specifies whether to
                allow the task, global channel, or custom scale to be edited
                in the DAQ Assistant. If allow_interactive_editing is True,
                the DAQ Assistant must support all task or global channel
                settings.
            allow_interactive_deletion (Optional[bool]): Specifies whether
                to allow the task, global channel, or custom scale to be
                deleted through MAX.
        """
        options = 0
        if overwrite_existing_channel:
            options |= _Save.OVERWRITE.value
        if allow_interactive_editing:
            options |= _Save.ALLOW_INTERACTIVE_EDITING.value
        if allow_interactive_deletion:
            options |= _Save.ALLOW_INTERACTIVE_DELETION.value

        self._interpreter.save_global_chan(self._handle, self._name, save_as, author, options)