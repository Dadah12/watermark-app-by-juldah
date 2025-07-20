# progressbar.py

import tkinter as tk
from tkinter import ttk

class ProgressBar:
    """
    A simple wrapper around ttk.Progressbar that includes an optional
    percentage label and supports both determinate and indeterminate modes.
    """

    def __init__(self, parent, length=300, orient='horizontal', mode='determinate', show_percent=True):
        """
        :param parent:   Tkinter parent widget
        :param length:   Pixel width of the bar
        :param orient:   'horizontal' or 'vertical'
        :param mode:     'determinate' or 'indeterminate'
        :param show_percent: whether to display a percentage label
        """
        # Container frame for bar + label
        self.frame = tk.Frame(parent)
        self.frame.pack(pady=10)

        # The actual progress bar widget
        self.progress = ttk.Progressbar(
            self.frame,
            orient=orient,
            length=length,
            mode=mode
        )
        self.progress.pack(side=tk.LEFT)

        # Optional percentage label (only in determinate mode)
        self.show_percent = show_percent and mode == 'determinate'
        if self.show_percent:
            self._label = tk.Label(self.frame, text='0%')
            self._label.pack(side=tk.LEFT, padx=(5, 0))

    def start(self, max_value=None, interval=10):
        """
        Begin the progress. In determinate mode, set the maximum.
        In indeterminate mode, start the animation.

        :param max_value: The total value for 100% (determinate only).
        :param interval:  Milliseconds between moves (indeterminate only).
        """
        if max_value is not None:
            # Switch to determinate and set maximum
            self.progress.config(mode='determinate', maximum=max_value, value=0)
            if self.show_percent:
                self._label.config(text='0%')
        else:
            # Switch to indeterminate and start auto-stepping
            self.progress.config(mode='indeterminate')
            self.progress.start(interval)

    def update(self, value):
        """
        Update the current value of a determinate bar, refreshing the label.

        :param value: New progress value between 0 and maximum.
        """
        if self.progress['mode'] == 'determinate':
            self.progress['value'] = value
            if self.show_percent:
                max_val = self.progress['maximum'] or 1
                percent = int((value / max_val) * 100)
                self._label.config(text=f'{percent}%')
        # Force UI refresh
        self.progress.update()

    def stop(self):
        """
        Stop any indeterminate animation and reset to zero.
        """
        if self.progress['mode'] == 'indeterminate':
            self.progress.stop()
        self.progress['value'] = 0
        if self.show_percent:
            self._label.config(text='0%')
